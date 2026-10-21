"""Pure numerical RevF metal motor-mount feature specification, mm.

No CAD runtime imports: shared by the native Fusion and CQ builders.
Custom parts remain DEVELOPMENT, with physical stiffness and pilot fit holds.
"""
def motor_mount_specs(axis,k,x,y,face):
    sy=130 if y>0 else -130
    out=[]
    def item(suffix,notes):
        row=dict(name='CBP-D402_'+axis+'_'+str(k)+'_'+suffix,notes=notes,operations=[])
        out.append(row);return row['operations']
    def box(ops,name,size,p,op='cut'):
        ops.append(dict(kind='box',name=name,size=size,p=p,op=op))
    def bore(ops,name,d,L,p,v=(0,0,1)):
        ops.append(dict(kind='cyl',name=name,d=d,L=L,p=p,axis=v,op='cut'))
    def rounded_window(ops,name,dy,dz,p,r):
        # Seven simple driven cuts form an exact rounded rectangle through X.
        xx,yy,zz=p
        box(ops,name+'-CORE-Y',(4.2,dy-2*r,dz),p)
        box(ops,name+'-CORE-Z',(4.2,dy,dz-2*r),p)
        for a in [-1,1]:
            for b in [-1,1]:
                bore(ops,name+'-R-'+str(a)+'-'+str(b),2*r,4.2,(xx-2.1,yy+a*(dy/2-r),zz+b*(dz/2-r)),(1,0,0))
    ops=item('TOP_BAR','6061-T6 saw/drill stock42x20x8. Four side M3 drill9/fullthread7 minimum; two5.5vertical M5 clearance atXoffsets+/-6mm. M3 axes offset5mm fromM5 so shafts do not intersect. Deburr0.2; underside driver access and preinserted HNTT5 required.')
    box(ops,'STOCK',(42,20,8),(x,sy,276),'new')
    for dx in [-6,6]:bore(ops,'M5-'+str(dx),5.5,8,(x+dx,sy,272))
    for side in [-1,1]:
        for dy in [-5,5]:bore(ops,'END-M3-'+str(side)+'-'+str(dy),2.5,9,(x+side*21,sy+dy,276),(-side,0,0))
    for foot in [-1,1]:
        ops=item(('REAR' if foot>0 else 'FRONT')+'_FOOT_BAR','6061-T6 stock42x14.3x6. M4 through taps, nominal6mm engagement. EndM3 drill9/fullthread7 minimum; M3 axesY32 versusM4Y27 keep shafts5mm apart. 0.2deburr. Verify tap fit and strip strength.')
        box(ops,'STOCK',(42,14.3,6),(x,y+foot*28.85,face-3),'new')
        for dx in [-17,17]:bore(ops,'M4-TAP-'+str(dx),3.3,6,(x+dx,y+foot*27,face-6))
        for side in [-1,1]:bore(ops,'END-M3-'+str(side),2.5,9,(x+side*21,y+foot*32,face-3),(-side,0,0))
        if y<0 and foot<0:
            for dx in [-6,6]:bore(ops,'M5-ALLEN-ACCESS-'+str(dx),6,6,(x+dx,sy,face-6))
        if (foot>0)==(y>0):
            for dx in [-9,9]:bore(ops,'CABLE-TAB-M3-'+str(dx),2.5,7,(x+dx,y+foot*36,face-3),(0,-foot,0))
    y0=min(y-36,sy-10);y1=max(y+36,sy+10);bottom=face-56.5
    for side in [-1,1]:
        xx=x+side*23
        label='OUTER' if side*x>0 else 'INNER'
        ops=item(label+'_CHEEK','6061-T6 sheet4. Waterjet/laser two-dimensional profile, body-windowR3; plate-windowR0.5. Minimum lowerUbridge5mm and motor-bottomgap3.5mm. Outer rail relief and front-inner idler step retained. No printed structural path. Static/dynamic stiffness and connector/pigtail envelope unvalidated.')
        box(ops,'SHEET-BLANK',(4,y1-y0,280-bottom),(xx,(y0+y1)/2,(bottom+280)/2),'new')
        rounded_window(ops,'MOTOR-ENVELOPE',49,52,(xx,y,face-25.5),3)
        rounded_window(ops,'PLATE-HEAD-ACCESS',64.2,12.1,(xx,y,face+5.95),.5)
        if side*x>0:
            box(ops,'Y-RAIL-PROFILE-CLEARANCE',(4.2,202,6),(xx,0,277.5))
        elif k==2:
            # The opposite-level front return extends across the inner cheek.
            # This stepped sheet outline is connected via its lower U bridge.
            box(ops,'FRONT-RETURN-STEP',(4.2,61,18),(xx,-89.5,271.3))
        for dy in [-5,5]:bore(ops,'TOP-M3-'+str(dy),3.3,4,(xx-2,sy+dy,276),(1,0,0))
        for foot in [-1,1]:bore(ops,'FOOT-M3-'+str(foot),3.3,4,(xx-2,y+foot*32,face-3),(1,0,0))
    # Flat strain-relief tab fixes outside the frame-side foot, clear of motor.
    sf=1 if y>0 else -1
    ops=item('CABLE_TIE_TAB','6061 sheet1.5 flat30x25, no bend. TwoM3x6 with0.5washers into frame-side foot4mm engagement; drill7/fullthread5.5 minimum, four2x5 tie slots. Route pigtail outside motor before lowerUbridge. Connector/bend radius HOLD pending actualmotor; protect all cable-contact edges.')
    box(ops,'TAB',(30,1.5,25),(x,y+sf*36.75,face-12.5),'new')
    for dx in [-9,9]:bore(ops,'FIX-M3-'+str(dx),3.3,1.5,(x+dx,y+sf*36,face-3),(0,sf,0))
    for dx in [-9,9]:
        for zz in [-13,-20]:box(ops,'TIE-'+str(dx)+'-'+str(zz),(2,1.7,5),(x+dx,y+sf*36.75,face+zz))
    return out
