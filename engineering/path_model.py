"""Optimistic path traversal study, not a firmware emulator or printable profile.

Units: mm, s, mm3. Forward/backward squared-speed passes with geometric
junction limits and trapezoidal/triangular acceleration. Inspired by Klipper's
documented centripetal junction geometry, independently implemented. Includes
retraction barriers and Z. Omits extrusion-ratio junction limits, minimum cruise
ratio, pressure advance, shaping, thermal dwell and finite lookahead; therefore
results are optimistic model scenarios, not measured print durations.
"""
import re, math, json, hashlib
from pathlib import Path
from dataclasses import dataclass
ROOT = Path(__file__).resolve().parents[1]
AF = math.pi*1.75**2/4

@dataclass
class Move:
    d: float
    u: tuple
    e: float
    z: float
    feed: float
    role: str
    width: float
    xyz: bool = True

def parse(path):
    pos=[0.,0.,0.]; feed=40.; relative_e=False; absolute_xyz=True
    epos=0.; role='unknown'; width=0.; moves=[]
    for raw in path.read_text().splitlines():
        if raw.startswith(';TYPE:'): role=raw.split(':',1)[1].strip()
        if raw.startswith(';WIDTH:'): width=float(raw.split(':',1)[1])
        s=raw.split(';',1)[0].strip()
        if not s: continue
        cmd=s.split()[0]
        if cmd=='M83': relative_e=True
        elif cmd=='M82': relative_e=False
        elif cmd=='G90': absolute_xyz=True
        elif cmd=='G91': absolute_xyz=False
        f={k:float(v) for k,v in re.findall(r'([XYZEF])(-?\d*\.?\d+)',s)}
        if cmd=='G92':
            if any(k in f for k in 'XYZ'): raise ValueError('XYZ reset unsupported')
            epos=f.get('E',epos)
        if cmd in ('G2','G3'): raise ValueError('Arc input unsupported')
        if cmd not in ('G0','G1'): continue
        if not absolute_xyz: raise ValueError('Relative XYZ unsupported')
        feed=f.get('F',feed*60)/60
        p=[f.get(k,pos[i]) for i,k in enumerate('XYZ')]
        delta=[p[i]-pos[i] for i in range(3)]; d=math.sqrt(sum(v*v for v in delta))
        e=f.get('E',0.) if relative_e else f.get('E',epos)-epos
        if not relative_e: epos=f.get('E',epos)
        pos=p
        if d>1e-9: moves.append(Move(d,tuple(v/d for v in delta),e,p[2],feed,role,width))
        elif abs(e)>1e-9: moves.append(Move(abs(e),(0.,0.,0.),e,p[2],feed,'pure-E',0.,False))
    dep=[i for i,m in enumerate(moves) if m.xyz and m.e>0]
    # Timing starts with first deposition and ends at last deposition.
    return moves[dep[0]:dep[-1]+1]

def duration(moves, flow=100., vmax=1500., accel=50000., scv=20.,
             first_layer_cap=None, honor_feed=False, corexy=False):
    n=len(moves); limits=[]; aa=[]
    jd=scv**2*(math.sqrt(2)-1)/accel
    for m in moves:
        if not m.xyz:
            v=min(40.,m.feed); a=5000.
        else:
            v=vmax; a=accel
            if honor_feed: v=min(v,m.feed)
            if m.e>0: v=min(v,flow*m.d/(m.e*AF),150.*m.d/m.e)
            if abs(m.u[2])>1e-9:
                v=min(v,30./abs(m.u[2])); a=min(a,1000./abs(m.u[2]))
            if corexy:
                # Same motor belt-speed limit as Cartesian, transformed A=x+y B=x-y.
                ratio=max(abs(m.u[0]+m.u[1]),abs(m.u[0]-m.u[1]))
                if ratio>0: v=min(v,vmax/ratio)
            if first_layer_cap is not None and m.z<=0.251 and m.e>0:
                v=min(v,first_layer_cap)
        limits.append(v*v); aa.append(a)
    junction=[0.]*(n+1)
    for i in range(1,n):
        prev,m=moves[i-1],moves[i]
        if not prev.xyz or not m.xyz: continue
        dot=max(-1.,min(1.,sum(x*y for x,y in zip(prev.u,m.u))))
        sh=math.sqrt((1+dot)/2); ch=math.sqrt((1-dot)/2)
        cap=min(limits[i-1],limits[i])
        if 1-sh>1e-12 and ch>1e-12:
            cap=min(cap,jd*min(aa[i-1],aa[i])*sh/(1-sh),
                    .5*min(prev.d*aa[i-1],m.d*aa[i])*sh/ch)
        junction[i]=cap
    for i,m in enumerate(moves):
        junction[i+1]=min(junction[i+1],junction[i]+2*aa[i]*m.d)
    for i in range(n-1,-1,-1):
        junction[i]=min(junction[i],junction[i+1]+2*aa[i]*moves[i].d)
    total=0.; dep_time=0.; peak_v=0.; peak_q=0.; layers={}
    for i,m in enumerate(moves):
        a=aa[i]; v0=math.sqrt(junction[i]); v1=math.sqrt(junction[i+1])
        vp=math.sqrt(min(limits[i],a*m.d+(junction[i]+junction[i+1])/2))
        ramp=(2*vp-v0-v1)/a
        cruise=max(0.,m.d-(2*vp*vp-v0*v0-v1*v1)/(2*a))/vp
        t=ramp+cruise; total+=t
        if m.xyz: peak_v=max(peak_v,vp)
        if m.xyz and m.e>0:
            dep_time+=t; peak_q=max(peak_q,vp*m.e*AF/m.d)
        layers[m.z]=layers.get(m.z,0)+t
    return dict(seconds=total,deposition_seconds=dep_time,peak_velocity_mm_s=peak_v,
                peak_flow_mm3_s=peak_q,shortest_layer_s=min(layers.values()),
                assumed_flow_cap_mm3_s=flow,assumed_vmax_mm_s=vmax,
                assumed_accel_mm_s2=accel,assumed_scv_mm_s=scv,
                first_layer_cap_mm_s=first_layer_cap,corexy_belt_limit=corexy)

def summarize(moves):
    dep=[m for m in moves if m.xyz and m.e>0]
    volume=sum(m.e for m in dep)*AF
    roles={}
    for m in dep: roles[m.role]=roles.get(m.role,0)+m.e*AF
    return dict(volume_mm3=volume,mass_g=volume*.00124,
                extrusion_path_mm=sum(m.d for m in dep),
                travel_path_mm=sum(m.d for m in moves if m.xyz and m.e<=0),
                pure_e_moves=sum(not m.xyz for m in moves),
                minimum_average_flow_55s=volume/55,minimum_average_flow_60s=volume/60,
                ideal_flow_only_s={str(q):volume/q for q in (50,75,100,150,200)},
                nominal_width_min_mm=min(m.width for m in dep),
                nominal_width_max_mm=max(m.width for m in dep),
                layer_count=len(set(m.z for m in dep)),volume_by_role_mm3=roles)

def run():
    results={}
    paths=[ROOT/'slicing/analysis.gcode']+sorted((ROOT/'slicing/variants').glob('*/analysis.gcode'))
    for path in paths:
        moves=parse(path); name=path.parent.name if 'variants' in str(path) else 'checkpoint-001'
        grid=[]
        for q in (50,75,100,150,200,500):
            for a in (20000,50000,100000):
                grid.append(duration(moves,q,1500,a,20))
        sensitivity=[duration(moves,200,v,a,s,fl,corexy=core)
                     for v,a,s,fl,core in [(2000,100000,100,None,False),
                         (1500,50000,20,100,False),(1500,50000,20,None,True),
                         (1000,30000,10,50,False)]]
        results[name]={'gcode_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
                       'summary':summarize(moves),'grid':grid,'sensitivity':sensitivity}
        print(name, json.dumps(results[name]['summary']), flush=True)
    (ROOT/'engineering/path_results.json').write_text(json.dumps(results,indent=2)+'\n')

if __name__=='__main__': run()
