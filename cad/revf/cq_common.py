"""Millimeter solid-CAD verification/export helpers for RevF.

These solids are editable through their source builders. STEP import does not
create Fusion's native sketch/feature history: retain the parallel Fusion
builders and do not describe offline exports as an executed Fusion checkpoint.
"""
from pathlib import Path
import hashlib
import json
import math
import cadquery as cq

DENSITIES = {'aluminum': 2.70, 'aluminium': 2.70, '6061': 2.70,
             'steel': 7.85, 'stainless': 7.9, 'asa': 1.07, 'abs': 1.05,
             'petg': 1.27, 'pa12': 1.02, 'pa-cf': 1.12,
             'carbon': 1.60, 'ptfe': 2.15, 'silicone': 1.15}


def solid(shape):
    return shape.val() if isinstance(shape,cq.Workplane) else shape


def cyl(diameter,length,start=(0,0,0),direction=(0,0,1)):
    return cq.Solid.makeCylinder(diameter/2,length,cq.Vector(*start),cq.Vector(*direction))


def drill(shape,diameter,length,start=(0,0,0),direction=(0,0,1)):
    return solid(shape).cut(cyl(diameter,length,start,direction))


def safe_name(name):
    return ''.join(c if c.isalnum() or c in '-_.' else '_' for c in name)


def _density(part):
    if part.get('density_g_cm3') is not None:return float(part['density_g_cm3'])
    material=part.get('material','').lower()
    return next((v for k,v in DENSITIES.items() if k in material), None)


def part_record(part):
    s=solid(part['shape']);bb=s.BoundingBox();c=s.Center()
    volume=s.Volume();density=_density(part)
    nominal=part.get('mass_g',part.get('mass_override_g'))
    proxy_mass=volume*density/1000 if density is not None else None
    mass=nominal if nominal is not None else proxy_mass
    return {k:v for k,v in part.items() if k!='shape'} | {
        'shape_valid':s.isValid(), 'solid_count':len(s.Solids()),
        'volume_mm3':volume,'density_g_cm3':density,
        'mass_g':mass,'mass_basis':'catalog/declared override' if nominal is not None else 'CAD volume times assumed material density',
        'geometric_mass_g':proxy_mass,
        'centroid_mm':[c.x,c.y,c.z],
        'bbox_mm':[[bb.xmin,bb.ymin,bb.zmin],[bb.xmax,bb.ymax,bb.zmax]],
    }


def exportAssembly(parts,folder,stem,individual=True,stl=True):
    folder=Path(folder);folder.mkdir(parents=True,exist_ok=True)
    assy=cq.Assembly(name=stem);records=[];files=[];seen=set()
    for part in parts:
        name=safe_name(part['name'])
        if name in seen:raise ValueError('Duplicate part instance '+name)
        seen.add(name)
        shape=solid(part['shape']);row=part_record(part)
        if not row['shape_valid']:raise ValueError('Invalid BRep '+name)
        color={'printed':(0.20,0.45,0.80),'cnc':(0.68,0.72,0.76),
               'purchased':(0.38,0.40,0.43),'fastener':(0.15,0.16,0.18)}.get(part.get('category'),(.5,.5,.5))
        assy.add(shape,name=name,color=cq.Color(*color))
        records.append(row)
        if individual:
            out=folder/(name+'.step');cq.exporters.export(shape,str(out));files.append(out)
            if stl and part.get('category')=='printed':
                out=folder/(name+'.stl');cq.exporters.export(shape,str(out),tolerance=.02,angularTolerance=.1);files.append(out)
    path=folder/(stem+'.step');assy.save(str(path));files.append(path)
    path=folder/(stem+'-parts.json');path.write_text(json.dumps(records,indent=2)+'\n');files.append(path)
    groups={}
    for row in records:
        g=row.get('motion_group','unassigned');groups.setdefault(g,[]).append(row)
    totals={}
    for g,rows in groups.items():
        known=[r for r in rows if r['mass_g'] is not None];m=sum(r['mass_g'] for r in known)
        totals[g]={'known_mass_g':m,'unknown_mass_parts':[r['name'] for r in rows if r['mass_g'] is None],
                   'COM_mm':[sum(r['mass_g']*r['centroid_mm'][i] for r in known)/m for i in range(3)] if m else None}
    manifest={'status':'offline development geometry; Fusion history execution and manufacturing release pending',
              'units':'mm,g','part_count':len(records),'mass_groups':totals,
              'files':[{'name':p.name,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in files]}
    (folder/(stem+'-manifest.json')).write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps({'stem':stem,'parts':len(parts),'valid':all(r['shape_valid'] for r in records),'mass_groups':totals},indent=2))
    return manifest


def interference(parts,min_volume=.1,skip_categories=('fastener',)):
    hits=[]
    for i,a in enumerate(parts):
        if a.get('category') in skip_categories:continue
        sa=solid(a['shape']);ba=sa.BoundingBox()
        for b in parts[i+1:]:
            if b.get('category') in skip_categories:continue
            sb=solid(b['shape']);bb=sb.BoundingBox()
            if any(getattr(ba,k+'max')<=getattr(bb,k+'min')+1e-5 or getattr(bb,k+'max')<=getattr(ba,k+'min')+1e-5 for k in 'xyz'):continue
            v=sa.intersect(sb).Volume()
            if v>min_volume:hits.append({'a':a['name'],'b':b['name'],'overlap_mm3':v})
    return hits
