"""Independent G-code dimensional/flow audit for the fixed-width Cura trial."""
import math,re,json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
AF=math.pi*1.75**2/4

def audit(path):
    xyz=[0.,0.,0.];absolute_e=True;epos=0.;role='unknown';layer=-1
    result={'path':str(path.relative_to(ROOT)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
            'max_permitted_width_mm':.5,'deposition_volume_mm3':0.,'roles':{},'layers':[],
            'certain_width_violations':[],'bounds_mm':[[math.inf]*3,[-math.inf]*3]}
    for lineno,raw in enumerate(path.read_text(encoding='utf-8').splitlines(),1):
        if raw.startswith(';TYPE:'):role=raw[6:]
        if raw.startswith(';LAYER:'):layer=int(raw[7:])
        code=raw.split(';')[0].strip()
        if not code:continue
        command=code.split()[0]
        fields={k:float(v) for k,v in re.findall(r'([XYZEF])([+-]?(?:\d+(?:\.\d*)?|\.\d+))',code)}
        if command=='M82':absolute_e=True
        if command=='M83':absolute_e=False
        if command=='G92':
            if any(k in fields for k in 'XYZ'):raise ValueError('Unsupported XYZ reset')
            epos=fields.get('E',epos)
        if command in ('G2','G3','G91'):raise ValueError('Unsupported arc or relative XYZ')
        if command not in ('G0','G1'):continue
        nxt=[fields.get(k,xyz[i]) for i,k in enumerate('XYZ')]
        distance=math.dist(xyz,nxt)
        extruded=fields.get('E',epos)-epos if absolute_e else fields.get('E',0.)
        if absolute_e:epos=fields.get('E',epos)
        if distance>0 and extruded>0:
            volume=extruded*AF;result['deposition_volume_mm3']+=volume
            r=result['roles'].setdefault(role,{'volume_mm3':0.,'segments':0,'path_mm':0.,'largest_raw_area_mm2':0.})
            r['volume_mm3']+=volume;r['path_mm']+=distance;r['segments']+=1
            r['largest_raw_area_mm2']=max(r['largest_raw_area_mm2'],volume/distance)
            # Cura rounds XYZ to .001mm and relative E to .00001mm.
            # A definite violation must survive their worst-case rounding bounds.
            min_area=max(0,extruded-.000005)*AF/(distance+math.sqrt(3)*.001)
            permitted_height=.5 if role=='FILL' else .25
            if min_area>.5*permitted_height+1e-9:
                result['certain_width_violations'].append({'line':lineno,'role':role,
                    'minimum_width_mm':min_area/permitted_height,'z':nxt[2]})
            if nxt[2] not in result['layers']:result['layers'].append(nxt[2])
            for p in (xyz,nxt):
                for i in range(3):
                    result['bounds_mm'][0][i]=min(result['bounds_mm'][0][i],p[i])
                    result['bounds_mm'][1][i]=max(result['bounds_mm'][1][i],p[i])
        xyz=nxt
    result['layer_count']=len(result['layers'])
    result['layer_steps_mm']=sorted(set(round(b-a,6) for a,b in zip(result['layers'],result['layers'][1:])))
    result['limitations']=['Flow audit uses Cura rectangular cross section and permitted .5mm combined infill thickness.',
        'Does not certify local infill stacking, two-wall coverage of every narrow feature, actual bead width, or physical dimensional accuracy.',
        'Header TIME:6666 and Filament used:0 are CLI placeholders, not measured values.',
        'No-gap variant omits optional fill between walls, while retaining thin-outline printing; physical pinholes/coverage require inspection.']
    return result

if __name__=='__main__':
    results={}
    for name in ('cura-4.13.1','cura-4.13.1-no-gap','cura-4.13.1-simplified'):
        r=audit(ROOT/'slicing'/name/'analysis.gcode');results[name]=r
        print(name,'volume',r['deposition_volume_mm3'],'violations',len(r['certain_width_violations']), 'bounds',r['bounds_mm'])
    (ROOT/'validation/cura-width-audit.json').write_text(json.dumps(results,indent=2)+'\n',encoding='utf-8')
