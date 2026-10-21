"""RevF frame closure, external gussets and low-compliance feet, world-mm.

Development geometry. New side-panel holes avoid the original panel/gusset
collisions. Printed gusset/feet creep and assembled stiffness are unvalidated.
No frame extrusion is duplicated. Run integration interference audit before
manufacture. HNTT5 drawing proxy omits minor edge lands/radii.
"""
from pathlib import Path
import math
import cadquery as cq
from cq_common import cyl,drill,exportAssembly

SOURCE='https://th.misumi-ec.com/en/vona2/detail/110302607960/?HissuCode=HNTT5-5'


def build():
    parts=[]
    def add(n,s,m='aluminum',cat='cnc',notes=''):
        parts.append(dict(name=n,shape=s,material=m,category=cat,motion_group='fixed',notes=notes))
    def box(w,d,h,p):return cq.Workplane('XY').box(w,d,h).translate(p).val()
    def vadd(a,b,k=1):return tuple(a[i]+b[i]*k for i in range(3))
    def bolt(n,p,axis,length):
        head=vadd(p,axis,-5)
        s=cyl(5,length,p,axis).fuse(cyl(8.5,5,head,axis))
        plane=cq.Plane(origin=vadd(head,axis,-.01),normal=axis,xDir=(0,1,0) if abs(axis[0])>.5 else (1,0,0))
        s=s.cut(cq.Workplane(plane).polygon(6,8/math.sqrt(3)).extrude(3.5).val())
        add(n,s,'steel','fastener','ISO4762 M5x'+str(length)+'; nominal threads omitted.')
    def washer(n,p,axis):
        add(n,cyl(10,1,p,axis).cut(cyl(5.3,1,p,axis)),'steel','fastener','M5 washer OD10xID5.3x1.')
    def tnut(n,p,inward,slot):
        # Official HNTT5:10x10,T4.1,E3.3,neck5.8,M5. Drawing
        # taper outline simplified; seated neck begins1.2 below exterior.
        u=cq.Vector(*inward).cross(cq.Vector(*slot))
        plane=cq.Plane(origin=vadd(p,slot,-5),normal=slot,xDir=u)
        pts=[(-2.9,1.2),(2.9,1.2),(2.9,2),(5,2),(2.9,5.3),(-2.9,5.3),(-5,2),(-2.9,2)]
        s=cq.Workplane(plane).polyline(pts).close().extrude(10).val()
        s=drill(s,4.2,4.1,vadd(p,inward,1.2),inward)
        add(n,s,'steel','fastener','MISUMI HNTT5-5 drawing proxy; source '+SOURCE+'; edge lands/radii omitted. Preinsert before assembly.')
    def mount(n,p,outward,slot,length,grip):
        # p is the extrusion exterior surface; grip excludes1mm washer.
        under=vadd(p,outward,grip+1)
        bolt(n+'_SCREW',under,tuple(-q for q in outward),length)
        washer(n+'_WASHER',vadd(p,outward,grip),outward)
        tnut(n+'_HNTT5',p,tuple(-q for q in outward),slot)
        parts[-3]['intentional_thread_mate']=n+'_HNTT5'

    gusset_holes=[]
    for sy in [-1,1]:
        for top in [False,True]:
            z=300 if top else 0;iz=-1 if top else 1
            holes=[(sy*140-sy*u,z+iz*v) for u,v in [(10,30),(10,55),(30,10),(55,10)]]
            gusset_holes.extend(holes)
            tri=[(sy*140,z),(sy*70,z),(sy*140,z+iz*70)]
            s=cq.Workplane('YZ').polyline(tri).close().extrude(8).translate((141.5,0,0))
            s=s.edges('|X').fillet(3).val()
            for y,zz in holes:s=drill(s,5.5,8,(141.5,y,zz),(1,0,0))
            for side in [-1,1]:
                label=('R' if side>0 else 'L')+('_REAR' if sy>0 else '_FRONT')+('_TOP' if top else '_BOTTOM')
                add('CBP-F120_GUSSET_'+label,s if side>0 else s.mirror('YZ'),'PA-CF','printed','70mm right-triangle legs,8thick,R3corners; fourM5 mounts. Joint creep/stiffness unvalidated.')

    simple=[(0,10),(0,290)]+[(y,270) for y in [-90,0,90]]+[(y,z) for y in [-130,130] for z in [100,160,220]]
    assert len(set(simple+gusset_holes))==27
    for side in [-1,1]:
        hand='L' if side<0 else 'R'
        panel=box(1.5,280,300,(side*140.75,0,150))
        for y,z in simple+gusset_holes:panel=drill(panel,5.5,1.5,(side*140,y,z),(side,0,0))
        add('CBP-F121_SIDE_SHEAR_PANEL_'+hand,panel,'aluminum','cnc','280x300x1.5;27uniqueholes. Slots are on20/40mmextrusions; match drill while frame square.')
        for i,(y,z) in enumerate(simple+gusset_holes,1):
            gusset=(y,z) in gusset_holes
            slot=(0,0,1) if abs(y)==130 else (0,1,0)
            mount('CBP-H701_SIDE_'+hand+str(i),(side*140,y,z),(side,0,0),slot,16 if gusset else 8,9.5 if gusset else 1.5)
    rear=box(280,1.5,300,(0,140.75,150))
    rearholes=[(x,z) for x in [-90,0,90] for z in [10,290]]+[(x,z) for x in [-130,130] for z in [50,110,190,250]]
    for x,z in rearholes:rear=drill(rear,5.5,1.5,(x,140,z),(0,1,0))
    add('CBP-F122_REAR_SHEAR_PANEL',rear,'aluminum','cnc','280x300x1.5;14holes. Front remains open. Deburr and edge trim near wiring.')
    for i,(x,z) in enumerate(rearholes,1):mount('CBP-H702_REAR_'+str(i),(x,140,z),(0,1,0),(0,0,1) if abs(x)==130 else (1,0,0),8,1.5)

    # Corner post cap screws were not created in the Z subsystem.
    for sx in [-1,1]:
        for sy in [-1,1]:
            label=str(sx)+'_'+str(sy)
            bolt('CBP-H703_CORNER_BOTTOM_'+label,(sx*130,sy*130,-1),(0,0,1),30)
            washer('CBP-H704_CORNER_BOTTOM_WASHER_'+label,(sx*130,sy*130,-1),(0,0,1))
            bolt('CBP-H705_CORNER_TOP_'+label,(sx*130,sy*130,301),(0,0,-1),30)
            washer('CBP-H706_CORNER_TOP_WASHER_'+label,(sx*130,sy*130,300),(0,0,1))
            parts[-4]['intentional_thread_mate']='CBP-F102_CORNER_'+str(sx*130)+'_'+str(sy*130)
            parts[-2]['intentional_thread_mate']='CBP-F102_CORNER_'+str(sx*130)+'_'+str(sy*130)
            x,y=sx*115,sy*130
            foot=cq.Workplane('XY').box(50,28,10).edges('|Z').fillet(4).translate((x,y,-5)).val()
            foot=drill(foot,5.5,10,(x,y,-10))
            foot=drill(foot,10.5,6,(x,y,-10))
            foot=drill(foot,12,7,(sx*130,y,-7))
            foot=drill(foot,8,10,(sx*130,y,-10))
            add('CBP-F123_RIGID_FOOT_'+label,foot,'PA-CF','printed','50x28x10. RecessedM5attachment; separate12mm posthead cavity/access. Rigidstand avoids a12mm soft spring under frame.')
            pad=cq.Workplane('XY').box(50,28,2).edges('|Z').fillet(4).translate((x,y,-11)).val()
            pad=drill(pad,5,2,(x,y,-12));pad=drill(pad,8,2,(sx*130,y,-12))
            add('CBP-F124_TPU_FOOT_PAD_'+label,pad,'TPU95A','printed','2mmthick,100%infill; bond tostand. Dynamiccompliance unmeasured; do not claim isolationfrequency.')
            bolt('CBP-H707_FOOT_M5X10_'+label,(x,y,-5),(0,0,1),10)
            washer('CBP-H708_FOOT_WASHER_'+label,(x,y,-5),(0,0,1))
            tnut('CBP-H709_FOOT_HNTT5_'+label,(x,y,0),(0,0,1),(1,0,0))
            parts[-3]['intentional_thread_mate']='CBP-H709_FOOT_HNTT5_'+label
    return parts


if __name__=='__main__':
    exportAssembly(build(),Path(__file__).parent/'exports'/'frame_bracing','CBP_RevF_Frame_Bracing_DEVELOPMENT')
