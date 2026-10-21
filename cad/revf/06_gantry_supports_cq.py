"""Split beam sockets, accessible carriage adapters, pulley forks and hangers.

World-mm development solids. Separate socket/adaptor connection allows rail
bolts to be fitted first; four socket screws are outside the carbon section.
All custom geometries here are new, not alterations of a purchased extrusion.
"""
from pathlib import Path
import math
import runpy
import cadquery as cq
from cq_common import cyl,drill,exportAssembly

_drive=runpy.run_path(str(Path(__file__).with_name('05_drives_cq.py')))
CX=_drive['CX'];R=_drive['R'];PLANES=_drive['PLANES']
MOTOR_FACE_OFFSET=_drive['MOTOR_FACE_OFFSET']


def box(w,d,h,p):return cq.Workplane('XY').box(w,d,h).translate(p).val()


def build():
    parts=[]
    def add(n,s,mat='ASA',cat='printed',motion='gantry',notes=''):
        assert s.isValid(),n+' invalid BRep'
        if cat in ('printed','cnc'):assert len(s.Solids())==1,(n,len(s.Solids()))
        parts.append(dict(name=n,shape=s,material=mat,category=cat,motion_group=motion,notes=notes))
    def bolt(n,p,axis,length,thread_mate=None):
        head=tuple(p[i]-3*axis[i] for i in range(3))
        s=cyl(3,length,p,axis).fuse(cyl(5.5,3,head,axis))
        plane=cq.Plane(origin=tuple(head[i]-.01*axis[i] for i in range(3)),normal=axis,xDir=(0,1,0) if abs(axis[0])>.5 else (1,0,0))
        s=s.cut(cq.Workplane(plane).polygon(6,5/math.sqrt(3)).extrude(2.3).val())
        add(n,s,'steel','fastener',notes='M3 socket head, nominal thread omitted; underhead length'+str(length)+'.')
        if thread_mate:parts[-1]['intentional_thread_mate']=thread_mate
    def washer(n,x,y,z):
        add(n,cyl(7,.5,(x,y,z)).cut(cyl(3.2,.5,(x,y,z))),'steel','fastener',notes='M3 washer OD7x0.5.')
    fork_stations=[(-14,259),(14,259),(-6,293),(14,293)]
    for side in [-1,1]:
        hand='R' if side>0 else 'L'
        # Right-hand local geometry; mirrored after cuts, never negative size.
        adapter=box(4,38,51,(104,0,279.5))
        for y in [-8,8]:
            for z in [272.5,287.5]:
                adapter=drill(adapter,3.3,4,(102,y,z),(1,0,0))
                adapter=drill(adapter,6,2.5,(102,y,z),(1,0,0))
        for y,z in fork_stations:adapter=drill(adapter,2.5,4,(102,y,z),(1,0,0))
        # Socket wall with 0.15mm nominal clearance on each tube face.
        socket=box(20,28,28,(65,0,280)).cut(box(20.2,20.3,20.3,(65,0,280)))
        socket=socket.fuse(box(20,18,8,(65,0,298)))
        socket=socket.cut(box(20.2,.8,22,(65,0,291.1)))
        # Rail ends atX70. Relief ends70.5 so the outer4.5mm front wall
        # still joins the upper clamp jaw to its lower half as one part.
        socket=socket.cut(box(15.7,5.6,8,(62.65,-12.5,280)))
        for x in [60,70]:
            socket=drill(socket,3.3,18,(x,-9,298),(0,1,0))
            # Hex nut trap, M3 AF5.5 plus0.2 fit allowance.
            hexnut=(cq.Workplane('XZ').center(x,298).polygon(6,5.7*2/math.sqrt(3)).extrude(2.6).translate((0,9,0)).val())
            socket=socket.cut(hexnut)
        for y in [-5,5]:
            socket=drill(socket,4.6,4,(65,y,298))
            socket=drill(socket,3.3,4,(65,y,294))
        forkplate=box(7,38,44,(98.5,0,276))
        for y,z in fork_stations:
            forkplate=drill(forkplate,3.3,7,(95,y,z),(1,0,0))
            forkplate=drill(forkplate,6,4,(95,y,z),(1,0,0))
        # Base fork sits below both idlers; rib remains1.25mm behind flange.
        fork=box(18,33,6,(CX,-28.5,260.0)).fuse(box(20,8,32.3,(92,-16,273.15)))
        forkplate=forkplate.fuse(fork)
        forkplate=drill(forkplate,5.2,6,(CX,-35,257))
        for x in [CX-6,CX+6]:forkplate=drill(forkplate,2.5,8,(x,-16,281.3))
        # Independent cap clearance and outer belt windows. The lower fork
        # attachment screws sit below beltB, not across its vertical strand.
        forkplate=forkplate.cut(box(18.4,33.4,6.4,(CX,-28.5,292.3)))
        for z in PLANES.values():forkplate=forkplate.cut(box(3.2,40.4,10,(100.6,0,z)))
        for y in [-8,8]:
            for z in [272.5,287.5]:forkplate=drill(forkplate,6.5,7,(95,y,z),(1,0,0))
        # Access lower rear screw from free space past the wide fork base.
        forkplate=drill(forkplate,6,24,(75,-14,259),(1,0,0))
        for y,z in fork_stations:forkplate=drill(forkplate,3.3,7,(95,y,z),(1,0,0))
        cap=box(18,33,6,(CX,-28.5,292.3))
        cap=drill(cap,5.2,6,(CX,-35,289.3))
        for x in [CX-6,CX+6]:
            cap=drill(cap,3.3,6,(x,-16,289.3))
            cap=drill(cap,6,3,(x,-16,292.3))
        bridge=box(50,38,4,(85,0,307))
        for y in [-10,10]:
            bridge=drill(bridge,3.3,4,(104,y,305));adapter=drill(adapter,2.5,4,(104,y,301))
        for y in [-5,5]:bridge=drill(bridge,3.3,4,(65,y,305))
        if side<0:
            adapter=adapter.mirror('YZ');socket=socket.mirror('YZ');cap=cap.mirror('YZ');forkplate=forkplate.mirror('YZ');bridge=bridge.mirror('YZ')
        add('CBP-M205_'+hand+'_CARRIAGE_ADAPTER',adapter,'6061','cnc',notes='4mmAl,Z254..305; MGNcounterbores6x2.5 useM3x4 giving2.5thread and0.60nominalbelt/headgap. ForkmountsM3x6,Z259/293; upperrearY-6. Verify tolerances before manufacture.')
        add('CBP-M206_'+hand+'_SPLIT_BEAM_CLAMP',socket,notes='Tune20.3coupon;closedCF150,clampX55..75;2M3crossclampsX60/70Z298. Rail-end relief endsX70.5,Y-15.3..-9.7,Z276..284; outer4.5mmwall preserves one connectedpart. 2insertpockets4.6x4 plus3.3screwexitpilot. NoCFbeltports.')
        add('CBP-M208_'+hand+'_SEPARATE_IDLER_FORK',forkplate,notes='SeparateforkM3x6ontoAladapter atZ259/293, upperrearY-6. OuterbeltwindowsX99..102.2 andMGNheadreliefs. Ribtop289.3; capnotch and lowerrearheadaccess. Shaft/retention HOLD.')
        add('CBP-M209_'+hand+'_AL_PORTAL_BRIDGE',bridge,'6061','cnc',notes='50x38x4,X60..110,Z305..309; addedouteredgewidthfor6mmM3edgedistance. 2M3x8intoAladapter;2M3x12intoclampinsertsvia3mmspacers;0.5washers.')
        for j,y in enumerate([-5,5]):
            s=cyl(7,3,(side*65,y,302)).cut(cyl(3.3,3,(side*65,y,302)))
            add('CBP-P410_'+hand+'_PORTAL_SPACER_'+str(j),s,'aluminum','purchased')
        add('CBP-M207_'+hand+'_REMOVABLE_IDLER_CAP',cap,notes='2M3x10capbolts, rail returns at269.3/282.3; use precision5shaft and inner-race spacers; exactshaftretention HOLD.')
        # Shaft and spacers are separate purchased interfaces. Retention is not
        # represented as a fictitious solid nut in an unsupported catalog size.
        add('CBP-P408_'+hand+'_5MM_IDLER_SHAFT_ALLOWANCE',cyl(5,42.8,(side*CX,-35,257)),'steel','purchased',notes='Ground5mmshaft geometry allowance; exact shoulder/groove/retention SKU not frozen. Do not manufacture fork before stack freeze.')
        for j,(z,h) in enumerate([(263,.3),(275.3,1),(288.3,1)]):
            s=cyl(8,h,(side*CX,-35,z)).cut(cyl(5.2,h,(side*CX,-35,z)))
            add('CBP-P409_'+hand+'_INNER_RACE_SPACER_'+str(j),s,'steel','purchased',notes='5.2ID8OD; thickness stack is provisional, measure actual idler bearings/flanges.')
        for j,(y,z) in enumerate(fork_stations,1):bolt('CBP-H601_'+hand+'_FORK_M3X6_'+str(j),(side*99,y,z),(side,0,0),6,'CBP-M205_'+hand+'_CARRIAGE_ADAPTER')
        for j,(y,z) in enumerate([(y,z) for y in [-8,8] for z in [272.5,287.5]],1):bolt('CBP-H602_'+hand+'_MGN_M3X4_'+str(j),(side*104.5,y,z),(side,0,0),4,'CBP-P202_MGN9H_Y_BLOCK_'+hand)
        for j,x in enumerate([CX-6,CX+6],1):bolt('CBP-H603_'+hand+'_CAP_M3X10_'+str(j),(side*x,-16,292.3),(0,0,-1),10,'CBP-M208_'+hand+'_SEPARATE_IDLER_FORK')
        for j,y in enumerate([-10,10],1):
            bolt('CBP-H604_'+hand+'_PORTAL_AL_M3X8_'+str(j),(side*104,y,309.5),(0,0,-1),8,'CBP-M205_'+hand+'_CARRIAGE_ADAPTER');washer('CBP-H605_'+hand+'_PORTAL_AL_WASHER_'+str(j),side*104,y,309)
        for j,y in enumerate([-5,5],1):
            bolt('CBP-H606_'+hand+'_PORTAL_CLAMP_M3X12_'+str(j),(side*65,y,309.5),(0,0,-1),12)
            washer('CBP-H607_'+hand+'_PORTAL_CLAMP_WASHER_'+str(j),side*65,y,309)
    # Four motor plates hang from underside extrusion slots. Pedestals lie
    # beyond the motor body in Y; width45 avoids the rail adapter at X116.
    for axis,z in PLANES.items():
        sign=1 if axis=='A' else -1;face=z-MOTOR_FACE_OFFSET
        for k,(x,y) in enumerate([(-sign*CX,95),(sign*CX,-105)],1):
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
            sx=1 if x>0 else -1
            hanger=hanger.cut(box(8,202,10,(sx*113,0,280)))
            # Socket heads/OD7 washers project above the metal motor plate.
            # Keep access cylinders through the hanger; front frame-cap
            # obstruction still requires fitting motor/plate before hanging.
            for dx in [-15.5,15.5]:
                for dy in [-15.5,15.5]:hanger=drill(hanger,8,280-(face+6),(x+dx,y+dy,face+6))
            if k==2:hanger=drill(hanger,28.5,26.2,(sign*(CX-2*R),-105,262.8))
            if axis=='A' and k==2:
                # The idler relief disconnects the upper inner wall in front
                # of the rear pedestal. Omit that unusable island explicitly;
                # both feet remain joined by the continuous outer wall.
                low=face+5.95;high=280.1
                hanger=hanger.cut(box(5.5,19.5,high-low,(x-20,-83.25,(low+high)/2)))
            add('CBP-D402_'+axis+'_FRAME_HANGER_'+str(k),hanger,motion='fixed',notes='Printed motorhangerdevelopment: railkeepoutX109..117,Y±101,Z275..285; frontR14.25idlerkeepoutZ262.8..289; motorheads/washers8mmaccesscylinders. FrameanchorspreservedY±130. A-front disconnectedupperinnerwall omitted; outerwalljoinsbothfeet. Fitmotor/platebeforehanging duefrontcaptoolobstruction. Narrowwebs/hotmotorcreep/cyclicstiffness unvalidated.')
    return parts


if __name__=='__main__':
    exportAssembly(build(),Path(__file__).parent/'exports'/'gantry_supports','CBP_RevF_Gantry_Supports_DEVELOPMENT')
