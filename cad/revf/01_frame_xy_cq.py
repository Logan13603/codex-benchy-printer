"""RevF frame and rail solids, matching native frame009, with drill interfaces.

World XYZ, mm. Supplier proxies omit root reliefs, raceways and screw threads.
Published extrusion/rail masses override simplified volume estimates.
"""
from pathlib import Path
import cadquery as cq
from cq_common import drill, cyl, exportAssembly


def section(length,wide=False):
    h=40 if wide else 20
    s=cq.Workplane('XY').rect(20,h).extrude(length).val()
    base=[(-3,12),(-3,8),(-6,8),(-6,7),(-3,4),(3,4),(6,7),(6,8),(3,8),(3,12)]
    for sign in [-1,1]:
        pts=[(x,sign*(y+h/2-10)) for x,y in base]
        s=s.cut(cq.Workplane('XY').polyline(pts).close().extrude(length).val())
        for off in [-10,10] if wide else [0]:
            pts=[(sign*y,x+off) for x,y in base]
            s=s.cut(cq.Workplane('XY').polyline(pts).close().extrude(length).val())
    for off in [-10,10] if wide else [0]:s=drill(s,4.2,length,(0,off,0))
    return s


def block(w,d,h,x=0,y=0,z=0):
    return cq.Workplane('XY').box(w,d,h).translate((x,y,z)).val()


def build():
    parts=[]
    def add(name,s,material,category='purchased',motion='fixed',mass=None,notes=''):
        row=dict(name=name,shape=s,material=material,category=category,motion_group=motion,notes=notes)
        if mass is not None:row['mass_override_g']=mass
        parts.append(row)
    for y in [-130,130]:
        for z in [10,290]:
            s=section(280).rotate((0,0,0),(0,1,0),90).translate((-140,y,z))
            for x in [-130,130]:s=drill(s,5.5,20,(x,y,z-10))
            add('CBP-F104_X_CAP_Y'+str(y)+'_Z'+str(z),s,'aluminum',mass=140,
                notes='HFS5-2020 cut280; through-cap M5 holes at posts. Catalog0.50kg/m.')
    for x in [-130,130]:
        for y in [-130,130]:
            add('CBP-F102_CORNER_'+str(x)+'_'+str(y),section(260).translate((x,y,20)),
                'aluminum',mass=130,notes='M5x0.8 end taps minimum12 useful, tap geometry schematic.')
        s=section(240).rotate((0,0,0),(1,0,0),90).translate((x,120,10))
        s=drill(s,5.5,20,(x,-38,0))
        add('CBP-F101_BOTTOM_Y_'+str(x),s,'aluminum',mass=120)
        s=section(240,True).rotate((0,0,0),(1,0,0),90).translate((x,120,280))
        s=drill(s,5.5,40,(x,-38,260))
        add('CBP-F103_UPPER_Y_'+str(x),s,'aluminum',mass=211.2,notes='HFS5-2040,0.88kg/m,strongaxisvertical.')
    # Fixed rail adapters and exact nominal hole patterns.
    for side in [-1,1]:
        hand='L' if side<0 else 'R';axis=(-side,0,0)
        s=block(4,230,36,side*118,0,280)
        for y in range(-90,91,20):s=drill(s,2.5,4,(side*120,y,280),axis)
        for y in [-100,0,100]:
            for z in [270,290]:s=drill(s,5.5,4,(side*120,y,z),axis)
        add('CBP-M201_Y_ADAPTER_'+hand,s,'6061-T6','cnc',notes='M3 taps;6M5 slot anchors; 230x36x4. Flatten mating face.')
        s=block(6.5,200,9,side*112.75,0,280)
        for y in range(-90,91,20):
            s=drill(s,3.5,6.5,(side*116,y,280),axis)
            s=drill(s,6,3.5,(side*113,y,280),axis)
        add('CBP-P201_MGN9_Y_RAIL_'+hand,s,'steel',mass=76,notes='10mm ends;10holes20pitch; raceways omitted.')
        # Full envelope with rail relief, not merely a floating mounting cap.
        s=block(10,39.9,20,side*111,0,280)
        s=s.cut(block(6.6,40,9.3,side*112.7,0,280))
        for y in [-8,8]:
            for z in [272.5,287.5]:s=drill(s,2.5,3,(side*106,y,z),(side,0,0))
        add('CBP-P202_MGN9H_Y_BLOCK_'+hand,s,'steel',motion='gantry',mass=26,notes='Catalog26g;15Zx16Y mount pattern, M3x3blind.')
    # Carbon beam is a hollow stock tube; all rail clearance holes are real.
    s=block(158,20,20,0,0,280).cut(block(158.2,17,17,0,0,280))
    for i in range(9):s=drill(s,2.3,1.5,(-60+15*i,-10,280),(0,1,0))
    add('CBP-M202_CARBON_X_TUBE_158',s,'carbon','cnc','gantry',notes='20x20x1.5 closed158tube; ends±79clearfixedbeltreturnsby1.85mm; no transverse belt ports. density1.6g/cm3assumed.')
    s=block(140,2,8,0,-7.5,280)
    for i in range(9):s=drill(s,1.6,2,(-60+15*i,-8.5,280),(0,1,0))
    add('CBP-M204_BONDED_M2_STRIP',s,'6061','cnc','gantry',notes='M2through tapped; bonded inside carbon. Bond coupon required.')
    s=block(140,4.8,7,0,-12.4,280)
    for i in range(9):
        x=-60+15*i;s=drill(s,2.3,4.8,(x,-10,280),(0,-1,0));s=drill(s,4.2,2.4,(x,-12.4,280),(0,-1,0))
    add('CBP-P203_MGN7_X_RAIL_140',s,'steel',motion='gantry',mass=30.8,notes='9holes15pitch,endmargin10mm;80mmXtravelwith30.8blockhas14.6mmmarginatbothends.')
    s=block(30.8,8,17,0,-14,280).cut(block(31,5,7.3,0,-12.5,280))
    for x in [-6.5,6.5]:
        for z in [274,286]:s=drill(s,1.6,2.5,(x,-18,z),(0,1,0))
    add('CBP-P204_MGN7H_X_BLOCK',s,'steel',motion='toolhead',mass=15,notes='Full envelope with rail relief; M2blind2.5mm. Raceways omitted.')
    return parts


if __name__=='__main__':
    exportAssembly(build(),Path(__file__).parent/'exports'/'frame_xy','CBP_RevF_Frame_XY_DEVELOPMENT')
