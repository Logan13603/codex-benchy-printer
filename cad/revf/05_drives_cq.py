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
CX=88.75
FRONT=-105.0
BACK=95.0
MOVING_Y=-35.0
PLANES={'A':282.3,'B':269.3}
MOTOR_FACE_OFFSET=24.5


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
        max_delta=max(abs(pitch_route(axis,x,y)[2]-ref) for x in [-40,0,40] for y in [-20,0,30])
        # From head's first anchor to rear motor's first tangent. Include
        # moving-idler quarterarc; dL/dx=Â±1,dL/dy=1.
        def driven(x,y):
            pts,_,_=pitch_route(axis,x,y)
            return math.dist(*pts[0])+math.dist(*pts[1])+math.pi*R/2
        dxy=[(driven(1,0)-driven(-1,0))/2,(driven(0,1)-driven(0,-1))/2]
        assert max_delta<1e-8,(axis,max_delta)
        assert max(abs(dxy[0]-(1 if axis=='A' else -1)),abs(dxy[1]+1))<1e-8,(axis,dxy)
        result[axis]={'pitch_length_mm':ref,'workspace_xy_mm':[80,50],'max_length_change_over_workspace_mm':max_delta,
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
            face=z-MOTOR_FACE_OFFSET
            s=box(42.3,42.3,48,(x,y,face-24))
            try:s=cq.Workplane(obj=s).edges('|Z').fillet(2).val()
            except Exception:pass
            s=s.fuse(cyl(22,2,(x,y,face)),cyl(5,35,(x,y,face)))
            s=s.cut(box(8,2,30,(x,y+3.5,face+20)))
            for dx in [-15.5,15.5]:
                for dy in [-15.5,15.5]:s=drill(s,2.5,4.5,(x+dx,y+dy,face-4.5))
            add('CBP-P401_'+axis+'_LDO_MOTOR_'+str(k),s,'mixed','purchased',mass=350,
                notes='LDO42STH48-2804AC(S35) maker drawing:42.3max,31pitchM3x4.5min,22pilotx2,5shaftx35Â±0.5; cableconnector envelope pending.')
            add('CBP-P402_'+axis+'_36T_DRIVE_'+str(k),pulley(x,y,z),notes='PROVISIONAL purchased 2GT36T9mm5bore;22.41toothOD27.5flangeOD12wide+8hub. Confirm SKU and owned stock.')
            # Fixed motor pattern; tension belongs at the belt anchors. Slots
            # could drive the neighboring return idler into a motor screw head.
            plate=cq.Workplane(obj=box(45,64,6,(x,y,face+3))).edges('|Z').fillet(2).val()
            plate=drill(plate,8,6,(x,y,face))
            plate=drill(plate,22.10,2.15,(x,y,face))
            for dx in [-15.5,15.5]:
                for dy in [-15.5,15.5]:
                    plate=drill(plate,3.5,6,(x+dx,y+dy,face))
            for dx in [-17,17]:
                for dy in [-27,27]:plate=drill(plate,4.4,6,(x+dx,y+dy,face))
            if k==2:
                for dx in [-6,6]:plate=drill(plate,6,6,(x+dx,-130,face))
            if axis=='A' and k==2:
                plate=drill(plate,28.5,.70,(CX-2*R,FRONT,263.10))
            assert plate.isValid() and len(plate.Solids())==1
            add('CBP-D401_'+axis+'_MOTOR_PLATE_'+str(k),plate,'6061','cnc',notes='45x64x6 with R2 XY corners; fixed 31mm motor pattern 4x3.5 and 4M4 anchors. Two front Ø6 Allen access holes match foot bars; use4mmAF key. 8mm through shaft bore; underside 22.10 nominal pilot socket 2.15 deep clears 2mm pilot. FINAL PILOT FIT HOLD pending maker tolerance/measurement. A-front only: R14.25 upper 0.70mm idler pocket floor263.10 preserves pilot register. Deburr0.2, flatness0.05, motor face parallel top0.05. Do not infer validated stiffness. Fixed belt/motor planes retained.')
            for j,(dx,dy) in enumerate([(dx,dy) for dx in [-15.5,15.5] for dy in [-15.5,15.5]],1):
                px,py=x+dx,y+dy;under=face+6.5
                screw=cyl(3,10,(px,py,under),(0,0,-1)).fuse(cyl(5.5,3,(px,py,under)))
                recess=cq.Workplane('XY').center(px,py).polygon(6,5/math.sqrt(3)).extrude(-2.3).translate((0,0,under+3.01)).val()
                add('CBP-H501_'+axis+'_MOTOR_'+str(k)+'_M3X10_'+str(j),screw.cut(recess),'steel','fastener',notes='M3x10 plus0.5washer;3.5mm motor thread engagement. Heads give0.60mm nominal lateral gap to belt strands; measure/tolerance check required.')
                parts[-1]['intentional_thread_mate']='CBP-P401_'+axis+'_LDO_MOTOR_'+str(k)
                wr=3.0 if axis=='A' and k==2 and dx<0 else 3.5
                add('CBP-H502_'+axis+'_MOTOR_'+str(k)+'_WASHER_'+str(j),ring(wr,1.6,.5,face+6,px,py),'steel','fastener',notes='M3 washer '+str(wr*2)+'ODx0.5; A-front inner pair OD6 for neighbor idler clearance. Nominal gap0.434mm needs tolerance stack.')
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
