"""Detailed RevF AWD CoreXY drive study, world mm.

Exact orthogonal pitch paths produce qA=x-y and qB=-x-y. These are
development drive interfaces: selected pulley/shaft SKUs and mount-access
checks remain release holds. The 9mm belt is mandatory; pitch/tooth count of
the owner's existing pulleys is unknown, so this builder explicitly assumes
2GT36T rather than asserting that stock fits.
"""
from pathlib import Path
import math
import cadquery as cq
from cq_common import cyl,drill,exportAssembly

R=36*2/(2*math.pi)
CX=93.0
FRONT=-105.0
BACK=95.0
MOVING_Y=-35.0
PLANES={'A':282.3,'B':269.3}


def box(w,d,h,p):return cq.Workplane('XY').box(w,d,h).translate(p).val()


def ring(ro,ri,h,z,x=0,y=0):return cyl(ro*2,h,(x,y,z)).cut(cyl(ri*2,h,(x,y,z)))


def sector(cx,cy,r,t,z,a0,a1):
    def p(rad,ang):return (cx+rad*math.cos(math.radians(ang)),cy+rad*math.sin(math.radians(ang)))
    mid=(a0+a1)/2
    wire=(cq.Workplane('XY').moveTo(*p(r+t/2,a0)).threePointArc(p(r+t/2,mid),p(r+t/2,a1))
          .lineTo(*p(r-t/2,a1)).threePointArc(p(r-t/2,mid),p(r-t/2,a0)).close())
    return wire.extrude(9).translate((0,0,z-4.5)).val()


def straight(a,b,z,t=1.38):
    dx,dy=b[0]-a[0],b[1]-a[1];length=math.hypot(dx,dy)
    return box(length,t,9,(0,0,z)).rotate((0,0,0),(0,0,1),math.degrees(math.atan2(dy,dx))).translate(((a[0]+b[0])/2,(a[1]+b[1])/2,0))


def pitch_route(axis,x=0,y=0):
    """Five straights and four arcs, with mirrored motor directions.

    A: head left lower -> moving left -> rear left motor -> front left
    return idler -> front right motor -> moving right -> head right upper.
    B mirrors X. Equal belt preload cancels the opposite head yaw couples.
    """
    sign=1 if axis=='A' else -1
    yy=y+MOVING_Y
    # A route: bottom anchor exits moving-left at its left tangent upward.
    pts=[((x-20,yy-R),(-CX,yy-R)),
         ((-CX-R,yy),(-CX-R,BACK)),
         ((-CX+R,BACK),(-CX+R,FRONT)),
         ((-CX+2*R,FRONT-R),(CX,FRONT-R)),
         ((CX+R,FRONT),(CX+R,yy)),
         ((CX,yy+R),(x+20,yy+R))]
    arcs=[(-CX,yy,-90,-180),(-CX,BACK,180,0),
          (-CX+2*R,FRONT,180,270),(CX,FRONT,270,360),(CX,yy,0,90)]
    # Angles of rear motor are clockwise 180 -> 0; all other signs follow
    # the local tangent. Geometry is identical for CW/CCW semicircle length.
    if sign<0:
        pts=[((-a[0],a[1]),(-b[0],b[1])) for a,b in pts]
        # x is reversed above; restore head coordinates by adding2*x.
        pts[0]=((x+20,yy-R),pts[0][1]);pts[-1]=(pts[-1][0],(x-20,yy+R))
        arcs=[(-cx,cy,180-a0,180-a1) for cx,cy,a0,a1 in arcs]
    length=sum(math.dist(a,b) for a,b in pts)+sum(abs(a1-a0)*math.pi/180*R for _,_,a0,a1 in arcs)
    return pts,arcs,length


def validate_kinematics():
    result={}
    for axis in ['A','B']:
        ref=pitch_route(axis)[2]
        max_delta=max(abs(pitch_route(axis,x,y)[2]-ref) for x in [-40,0,40] for y in [-40,0,40])
        # From head's first anchor to rear motor's first tangent. Include
        # moving-idler quarterarc; dL/dx=±1,dL/dy=1.
        def driven(x,y):
            pts,_,_=pitch_route(axis,x,y)
            return math.dist(*pts[0])+math.dist(*pts[1])+math.pi*R/2
        dxy=[(driven(1,0)-driven(-1,0))/2,(driven(0,1)-driven(0,-1))/2]
        assert max_delta<1e-8,(axis,max_delta)
        assert max(abs(dxy[0]-(1 if axis=='A' else -1)),abs(dxy[1]+1))<1e-8,(axis,dxy)
        result[axis]={'pitch_length_mm':ref,'max_length_change_over_80mm_workspace':max_delta,
                      'first_anchor_to_rear_motor_derivative_XY':dxy,
                      'note':'motor sign can be inverted in firmware; paired motors must be phased before tensioning'}
    return result


def pulley(x,y,z,idler=False):
    # Cylindrical purchased tooth envelope; manufacturing tooth profile omitted.
    s=ring(22.41/2,2.5,10,z-5,x,y)
    s=s.fuse(ring(13.75,2.5,1,z-6,x,y),ring(13.75,2.5,1,z+5,x,y))
    if idler:
        s=drill(s,16,5,(x,y,z-6));s=drill(s,16,5,(x,y,z+1))
    else:
        s=s.fuse(ring(6,2.5,8,z-14,x,y))
        s=drill(s,2.5,5,(x+6,y,z-10),(-1,0,0));s=drill(s,2.5,5,(x,y+6,z-10),(0,-1,0))
    return s


def build():
    parts=[]
    def add(n,s,m='aluminum',cat='purchased',motion='fixed',mass=None,notes=''):
        p=dict(name=n,shape=s,material=m,category=cat,motion_group=motion,notes=notes)
        if mass is not None:p['mass_override_g']=mass
        parts.append(p)
    for axis,z in PLANES.items():
        sign=1 if axis=='A' else -1
        for k,(x,y) in enumerate([(-sign*CX,BACK),(sign*CX,FRONT)],1):
            face=z-21
            s=box(42.3,42.3,48,(x,y,face-24))
            try:s=cq.Workplane(obj=s).edges('|Z').fillet(2).val()
            except Exception:pass
            s=s.fuse(cyl(22,2,(x,y,face)),cyl(5,35,(x,y,face)))
            s=s.cut(box(8,2,30,(x,y+3.5,face+20)))
            for dx in [-15.5,15.5]:
                for dy in [-15.5,15.5]:s=drill(s,2.5,4.5,(x+dx,y+dy,face-4.5))
            add('CBP-P401_'+axis+'_LDO_MOTOR_'+str(k),s,'mixed','purchased',mass=350,
                notes='LDO42STH48-2804AC(S35) maker drawing:42.3max,31pitchM3x4.5min,22pilotx2,5shaftx35±0.5; cableconnector envelope pending.')
            add('CBP-P402_'+axis+'_36T_DRIVE_'+str(k),pulley(x,y,z),notes='PROVISIONAL purchased 2GT36T9mm5bore;22.41toothOD27.5flangeOD12wide+8hub. Confirm SKU and owned stock.')
            # Motor plate: four screw slots permit radial tension adjustment.
            plate=box(45,64,6,(x,y,face+3));plate=drill(plate,23,6,(x,y,face))
            for dx in [-15.5,15.5]:
                for dy in [-15.5,15.5]:
                    slot=cq.Workplane('XY').center(x+dx,y+dy).slot2D(7.5,3.5,90).extrude(6).translate((0,0,face)).val();plate=plate.cut(slot)
            for dx in [-17,17]:
                for dy in [-27,27]:plate=drill(plate,4.4,6,(x+dx,y+dy,face))
            add('CBP-D401_'+axis+'_MOTOR_PLATE_'+str(k),plate,'6061','cnc',notes='45x64x6;3.5wide7.5longmountslots,4M4anchors. Narrow45width clears Yrailadapter by0.5mm; check alignment tolerances.')
        ix=sign*(-CX+2*R)
        add('CBP-P403_'+axis+'_RETURN_IDLER',pulley(ix,FRONT,z,True),notes='PROVISIONAL 36T9mm idler,2x625bearing5x16x5,groove/flange width requires vendor freeze.')
        for j,zz in enumerate([z-6,z+1]):
            add('CBP-P404_'+axis+'_RETURN_625_'+str(j),ring(8,2.5,5,zz,ix,FRONT),'steel',mass=5.0)
        for side in [-1,1]:
            x=side*CX
            add('CBP-P405_'+axis+'_MOVING_IDLER_'+str(side),pulley(x,MOVING_Y,z,True),motion='gantry',notes='Two625bearings not separately modeled in moving pulley; mass pending exact assembly.')
            for j,zz in enumerate([z-6,z+1]):
                add('CBP-P407_'+axis+'_MOVING_625_'+str(side)+'_'+str(j),ring(8,2.5,5,zz,x,MOVING_Y),'steel',motion='gantry',mass=5.0)
        pts,arcs,length=pitch_route(axis)
        pieces=[straight(a,b,z) for a,b in pts]+[sector(cx,cy,R,1.38,z,a0,a1) for cx,cy,a0,a1 in arcs]
        add('CBP-P406_'+axis+'_9MM_BELT_ROUTE',cq.Compound.makeCompound(pieces),'rubber','purchased','belt_distributed',
            notes='Continuous pitch route represented by touching solids; actual2GTteeth omitted. Nominal length %.2f plusclampengagement; cuttolength.'%length)
    return parts


if __name__=='__main__':
    import json
    print(json.dumps(validate_kinematics(),indent=2))
    exportAssembly(build(),Path(__file__).parent/'exports'/'drives','CBP_RevF_AWD_Drives_DEVELOPMENT')
