"""Partition one unchanged deposited centerline set between independent heads.

Optimistic scheduling screen: each layer is a barrier; each head preserves
original segment order. Repositioning is included, but collision avoidance,
retraction, seam bonding, synchronization and real extrusion dynamics are not.
This generates calculations, never printer G-code or a claimed compliant entry.
"""
import json, math
from collections import defaultdict
from path_model import ROOT, parse, Move, AF, duration, summarize


def split_segments(raw, axis, boundaries):
    layers = defaultdict(lambda: [[] for _ in range(len(boundaries)+1)])
    p = [0., 0., 0.]
    for move in raw:
        end = [p[i] + move.u[i]*move.d for i in range(3)]
        if move.xyz and move.e > 0:
            cuts = [0., 1.]
            delta = end[axis] - p[axis]
            if abs(delta) > 1e-10:
                cuts += [(b-p[axis])/delta for b in boundaries if 0 < (b-p[axis])/delta < 1]
            cuts.sort()
            for lo, hi in zip(cuts[:-1], cuts[1:]):
                a = tuple(p[i]+(end[i]-p[i])*lo for i in range(2))
                b = tuple(p[i]+(end[i]-p[i])*hi for i in range(2))
                mid = (a[axis]+b[axis])/2
                owner = sum(mid > divider for divider in boundaries)
                layers[move.z][owner].append((a, b, move.e*(hi-lo), move.role))
        p = end
    return layers


def head_paths(layers):
    count = len(next(iter(layers.values())))
    positions = [None] * count
    result = []
    for z, heads in sorted(layers.items()):
        paths = []
        for owner, segments in enumerate(heads):
            path = []
            if segments and positions[owner] is None:
                positions[owner] = segments[0][0]  # preposition before first print
            for a, b, e, role in segments:
                previous = positions[owner]
                distance = math.dist(previous, a)
                if distance > 1e-9:
                    path.append(Move(distance, ((a[0]-previous[0])/distance, (a[1]-previous[1])/distance, 0.), 0., z, 2400., 'parallel-travel', 0.))
                distance = math.dist(a, b)
                if distance > 1e-9:
                    path.append(Move(distance, ((b[0]-a[0])/distance, (b[1]-a[1])/distance, 0.), e, z, 2400., role, 0.))
                positions[owner] = b
            paths.append(path)
        result.append((z, paths))
    return result


def timing(paths, flow, velocity, acceleration, scv, floor=.2):
    total = 0.; rows = []
    previous_z = None
    for z, heads in paths:
        times = [duration(p, flow, velocity, acceleration, scv, first_layer_cap=300)['seconds'] if p else 0. for p in heads]
        # Shared bed Z moves between barriers, starts/stops at rest. 30mm/s,
        # 1000mm/s²; 0.25mm is triangular. Initial layer preposition excluded.
        dz = 0. if previous_z is None else z-previous_z
        ztime = 2*math.sqrt(dz/1000) if dz <= .9 else dz/30+.03
        layer = max(max(times), floor) + ztime
        total += layer; previous_z = z
        rows.append({'z_mm':z, 'head_times_s':times, 'elapsed_s':layer})
    return {'flow_per_head_mm3_s':flow, 'velocity_mm_s':velocity, 'acceleration_mm_s2':acceleration,
            'scv_mm_s':scv, 'minimum_layer_floor_s':floor, 'seconds':total, 'layers':rows}


def run():
    raw = parse(ROOT/'slicing/cura-4.13.1-simplified/analysis.gcode')
    xy = [0.,0.]; low = [math.inf]*2; high = [-math.inf]*2
    for m in raw:
        for k in (0,1):
            xy[k] += m.u[k]*m.d
            low[k] = min(low[k], xy[k]); high[k] = max(high[k], xy[k])
    result = {'status':'Optimistic independent-head screen; collisions and physical seams unresolved',
              'source_volume_mm3':summarize(raw)['volume_mm3'], 'cases':[]}
    for axis, count in [(0,2),(1,2),(1,3),(1,4)]:
        bounds = [low[axis]+(high[axis]-low[axis])*i/count for i in range(1,count)]
        layers = split_segments(raw, axis, bounds)
        paths = head_paths(layers)
        volume = sum(m.e*AF for _, heads in paths for p in heads for m in p if m.e>0)
        assert abs(volume-result['source_volume_mm3'])<1e-6
        rows = [timing(paths,q,1500,a,50) for q in (75,100,150) for a in (100000,250000,500000)]
        best = min(rows,key=lambda r:r['seconds'])
        case = {'split_axis':'XY'[axis], 'head_count':count, 'boundaries_mm_relative_origin':bounds,
                'deposited_volume_mm3':volume,
                'reposition_distance_mm':sum(m.d for _, hs in paths for p in hs for m in p if m.e<=0),
                'segment_count':sum(len(p) for _,hs in paths for p in hs),
                'grid':[{k:v for k,v in row.items() if k!='layers'} for row in rows],
                'fastest_layer_detail':best}
        result['cases'].append(case)
        print('split', 'XY'[axis], 'heads',count,'best',best['seconds'],flush=True)
        if axis==1 and count==2:
            expanded=[]
            for q in (150,200):
                for a in (500000,1000000):
                    for scv in (100,250,500):
                        r=timing(paths,q,2400,a,scv,.2);r.pop('layers');expanded.append(r)
            (ROOT/'engineering/parallel-head-expanded-results.json').write_text(json.dumps({
                'status':'Optimistic two-head Y-partition; no collisions or seam validation',
                'runs':expanded},indent=2)+'\n',encoding='utf-8')
    (ROOT/'engineering/parallel-head-results.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')


if __name__=='__main__': run()
