"""Split beam sockets, accessible carriage adapters, pulley forks and hangers.

World-mm development solids. Separate socket/adaptor connection allows rail
bolts to be fitted first; four socket screws are outside the carbon section.
All custom geometries here are new, not alterations of a purchased extrusion.
"""
from pathlib import Path
import math
import cadquery as cq
from cq_common import cyl,drill,exportAssembly


def box(w,d,h,p):return cq.Workplane('XY').box(w,d,h).translate(p).val()


def build():
    parts=[]
    def add(n,s,mat='ASA',cat='printed',motion='gantry',notes=''):
        parts.append(dict(name=n,shape=s,material=mat,category=cat,motion_group=motion,notes=notes))
    for side in [-1,1]:
        hand='R' if side>0 else 'L'
        # Right-hand local geometry; mirrored after cuts, never negative size.
        adapter=box(4,38,43,(104,0,283.5))
        for y in [-8,8]:
            for z in [272.5,287.5]:adapter=drill(adapter,3.3,4,(102,y,z),(1,0,0))
        for y in [-14,14]:
            for z in [267,293]:adapter=drill(adapter,2.5,4,(102,y,z),(1,0,0))
        # Socket wall with 0.15mm nominal clearance on each tube face.
        socket=box(20,28,28,(69,0,280)).cut(box(20.2,20.3,20.3,(69,0,280)))
        socket=socket.fuse(box(20,18,8,(69,0,298)))
        socket=socket.cut(box(20.2,.8,22,(69,0,291.1)))
        for x in [64,74]:
            socket=drill(socket,3.3,18,(x,-9,298),(0,1,0))
            # Hex nut trap, M3 AF5.5 plus0.2 fit allowance.
            hexnut=(cq.Workplane('XZ').center(x,298).polygon(6,5.7*2/math.sqrt(3)).extrude(2.6).translate((0,9,0)).val())
            socket=socket.cut(hexnut)
        for y in [-5,5]:socket=drill(socket,4.6,4,(69,y,298))
        forkplate=box(7,38,36,(98.5,0,280))
        for y in [-14,14]:
            for z in [267,293]:
                forkplate=drill(forkplate,3.3,7,(95,y,z),(1,0,0))
                forkplate=drill(forkplate,6,4,(95,y,z),(1,0,0))
        # Base fork sits below both idlers; rib remains1.25mm behind flange.
        fork=box(18,33,6,(93,-28.5,260.0)).fuse(box(12,8,37,(93,-16,275.5)))
        forkplate=forkplate.fuse(fork)
        forkplate=drill(forkplate,5.2,6,(93,-35,257))
        for x in [87,99]:forkplate=drill(forkplate,2.5,8,(x,-16,286))
        cap=box(18,33,6,(93,-28.5,292.3))
        cap=drill(cap,5.2,6,(93,-35,289.3))
        for x in [87,99]:cap=drill(cap,3.3,6,(x,-16,289.3))
        bridge=box(42,38,4,(85,0,307))
        for y in [-10,10]:
            bridge=drill(bridge,3.3,4,(104,y,305));adapter=drill(adapter,2.5,4,(104,y,301))
        for y in [-5,5]:bridge=drill(bridge,3.3,4,(69,y,305))
        if side<0:
            adapter=adapter.mirror('YZ');socket=socket.mirror('YZ');cap=cap.mirror('YZ');forkplate=forkplate.mirror('YZ');bridge=bridge.mirror('YZ')
        add('CBP-M205_'+hand+'_CARRIAGE_ADAPTER',adapter,'6061','cnc',notes='4mmAl; MG N9HboltsM3x6 first; four external socket M3x10 bolts into M3 taps. No fastener hidden by carbon after assembly.')
        add('CBP-M206_'+hand+'_SPLIT_BEAM_CLAMP',socket,notes='Tune20.3socket coupon;closedCF158;2M3crossclampsatZ298;2M3heat-inserts4.6ODx4inupperflange;3mmmetalspacersbelowAlportal. NoCFbeltports.')
        add('CBP-M208_'+hand+'_SEPARATE_IDLER_FORK',forkplate,notes='SeparateforkboltsM3x10ontoAlcarriageadapter; CFclampjoinsviametaltopportal. Precisionidlerstack/retention HOLD.')
        add('CBP-M209_'+hand+'_AL_PORTAL_BRIDGE',bridge,'6061','cnc',notes='42x38x4, Z305..309; bypassesfixedreturnsaboveZ286.8;2M3x8intoAladapterand2M3x12intoclampinsertsvia3mmspacers.')
        for j,y in enumerate([-5,5]):
            s=cyl(7,3,(side*69,y,302)).cut(cyl(3.3,3,(side*69,y,302)))
            add('CBP-P410_'+hand+'_PORTAL_SPACER_'+str(j),s,'aluminum','purchased')
        add('CBP-M207_'+hand+'_REMOVABLE_IDLER_CAP',cap,notes='2M3x10capbolts, rail returns at269.3/282.3; use precision5shaft and inner-race spacers; exactshaftretention HOLD.')
        # Shaft and spacers are separate purchased interfaces. Retention is not
        # represented as a fictitious solid nut in an unsupported catalog size.
        add('CBP-P408_'+hand+'_5MM_IDLER_SHAFT_ALLOWANCE',cyl(5,42.8,(side*93,-35,257)),'steel','purchased',notes='Ground5mmshaft geometry allowance; exact shoulder/groove/retention SKU not frozen. Do not manufacture fork before stack freeze.')
        for j,(z,h) in enumerate([(263,.3),(275.3,1),(288.3,1)]):
            s=cyl(8,h,(side*93,-35,z)).cut(cyl(5.2,h,(side*93,-35,z)))
            add('CBP-P409_'+hand+'_INNER_RACE_SPACER_'+str(j),s,'steel','purchased',notes='5.2ID8OD; thickness stack is provisional, measure actual idler bearings/flanges.')
    # Four motor plates hang from underside extrusion slots. Pedestals lie
    # beyond the motor body in Y; width45 avoids the rail adapter at X116.
    for axis,z in [('A',282.3),('B',269.3)]:
        sign=1 if axis=='A' else -1;face=z-21
        for k,(x,y) in enumerate([(-sign*93,95),(sign*93,-105)],1):
            frame_y=130 if y>0 else -130
            top=box(45,20,7,(x,frame_y,276.5))
            for dx in [-15,15]:top=drill(top,5.5,7,(x+dx,frame_y,273))
            hanger=top
            # Outside-Y crossmembers sit below motor plate, clear body42.3.
            for dy in [-27,27]:
                foot=box(42,8,6,(x,y+dy,face-3))
                for dx in [-17,17]:
                    foot=drill(foot,4.4,6,(x+dx,y+dy,face-6))
                    trap=(cq.Workplane('XY').center(x+dx,y+dy).polygon(6,7.2*2/math.sqrt(3)).extrude(3.3).translate((0,0,face-5.7)).val())
                    foot=foot.cut(trap)
                hanger=hanger.fuse(foot)
            # Two narrow side walls, inside rail adapter, bridge feet to cap.
            y0=min(y-31,frame_y-10);y1=max(y+31,frame_y+10)
            for dx in [-20,20]:
                wall=box(5,y1-y0,280-(face-6),(x+dx,(y0+y1)/2,(face-6+280)/2))
                # Remove central motor-body region below mounting face.
                wall=wall.cut(box(43,43,60,(x,y,face-30)))
                # Clear motor plate; leave outside45mm boundary untouched.
                wall=wall.cut(box(45.1,64.1,6.1,(x,y,face+3)))
                hanger=hanger.fuse(wall)
            add('CBP-D402_'+axis+'_FRAME_HANGER_'+str(k),hanger,motion='fixed',notes='Printed motor hanger draft: twoM5x12upperTnuts;4M4x12plateanchors with captive nuts; screw/toolaccess and hotmotor creep require validation.')
    return parts


if __name__=='__main__':
    exportAssembly(build(),Path(__file__).parent/'exports'/'gantry_supports','CBP_RevF_Gantry_Supports_DEVELOPMENT')
