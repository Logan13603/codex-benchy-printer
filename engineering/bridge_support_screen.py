"""Geometric support screen for concentric SKIN strokes.
A point outside the preceding STL cross-section lacks underlying model volume.
This favorable solid-model test does not model actual sparse infill or bead width.
"""
import sys,json,struct,hashlib,math,re
from pathlib import Path
from path_model import ROOT


def section(tri,z):
 x=tri[(tri[:,:,2].min(axis=1)<=z)&(tri[:,:,2].max(axis=1)>z)]
 pieces=[]
 for t in x:
  points=[]
  for i,j in ((0,1),(1,2),(2,0)):
   a,b=t[i],t[j]
   if (a[2]>z)!=(b[2]>z):points.append(a[:2]+(b[:2]-a[:2])*(z-a[2])/(b[2]-a[2]))
  if len(points)==2 and np.linalg.norm(points[1]-points[0])>1e-9:pieces.append(points)
 return np.asarray(pieces).reshape(-1,2,2)


def inside(points,segments):
 result=np.zeros(len(points),dtype=bool)
 if not len(segments):return result
 a,b=segments[:,0],segments[:,1]
 # Chunking avoids a full points*segments array for a large skin region.
 for start in range(0,len(points),512):
  p=points[start:start+512];y=p[:,1,None]
  crossing=(a[None,:,1]>y)!=(b[None,:,1]>y)
  dy=b[:,1]-a[:,1];safe=np.where(dy==0,1.,dy)
  x=a[None,:,0]+(y-a[None,:,1])*(b[:,0]-a[:,0])/safe
  result[start:start+len(p)]=np.sum(crossing&(x>p[:,0,None]),axis=1)%2==1
 return result


def skin_strokes(path):
 pos=np.zeros(3);role='';groups=[];active=None;rele=False;ep=0.
 for line in path.read_text(encoding='utf-8').splitlines():
  if line.startswith(';TYPE:'):
   role=line.split(':',1)[1].strip();active=None
  s=line.split(';')[0].strip();cmd=s.split()[0] if s else ''
  if cmd=='M83':rele=True
  if cmd=='M82':rele=False
  f={k:float(v) for k,v in re.findall(r'([XYZEF])(-?\d*\.?\d+)',s)}
  if cmd=='G92':ep=f.get('E',ep)
  if cmd not in ('G0','G1'):continue
  end=np.array([f.get(k,pos[i]) for i,k in enumerate('XYZ')]);e=f.get('E',0.) if rele else f.get('E',ep)-ep
  if not rele:ep=f.get('E',ep)
  if e>0 and role=='SKIN' and np.linalg.norm(end[:2]-pos[:2])>1e-9:
   if active is None or abs(active['z']-end[2])>1e-9:
    active={'z':float(end[2]),'points':[pos[:2].copy()]};groups.append(active)
   active['points'].append(end[:2].copy())
  else:active=None
  pos=end
 return groups


def run(trial="concentric-skin", output="concentric-support-screen.json", figure="concentric-support-008.png"):
 b=(ROOT/'slicing/models/3DBenchy.stl').read_bytes();n=struct.unpack_from('<I',b,80)[0]
 tri=np.frombuffer(b,dtype=np.dtype([('n','<f4',(3,)),('v','<f4',(3,3)),('attr','<u2')]),offset=84,count=n)['v'].astype(float)
 bounds=[tri.min(axis=(0,1)),tri.max(axis=(0,1))];offset=np.array([40.,40.])-(bounds[0][:2]+bounds[1][:2])/2
 tri[:,:,:2]+=offset
 rect=np.array([[[0,0],[2,0]],[[2,0],[2,1]],[[2,1],[0,1]],[[0,1],[0,0]]])
 assert inside(np.array([[1,.5],[3,.5],[-.1,.5],[1,2]]),rect).tolist()==[True,False,False,False]
 path=ROOT/'slicing/cura-travel-study'/trial/'analysis.gcode';groups=skin_strokes(path);sections={};rows=[];off_top=[]
 for number,g in enumerate(groups):
  if g['z']<=.5:continue
  z=g['z']-.25-.125
  if z not in sections:sections[z]=section(tri,z)
  p=np.asarray(g['points']);samples=[];weights=[]
  for a,b in zip(p[:-1],p[1:]):
   length=float(np.linalg.norm(b-a));count=max(1,math.ceil(length/.25))
   samples.extend(a+(np.arange(count)[:,None]+.5)/count*(b-a));weights.extend([length/count]*count)
  samples=np.asarray(samples);weights=np.array(weights);supported=inside(samples,sections[z]);fraction=float(weights[~supported].sum()/weights.sum())
  closed=float(np.linalg.norm(p[-1]-p[0]))<.005
  row={'stroke':number,'z_mm':g['z'],'length_mm':float(weights.sum()),'closed':closed,'unsupported_length_fraction':fraction}
  if fraction>.01:rows.append(row)
  if closed and fraction>.5:off_top.append((row,p,sections[z]))
 result={'status':'Model-volume support screen only; not slicer compliance or physical bridge validation',
         'gcode_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'mesh_to_gcode_xy_offset_mm':offset.tolist(),
         'layer_section_assumption':'Cura layer center Z-0.125; preceding layer center Z-0.375. Mesh recentered to80x80 bed bbox center.',
         'sample_spacing_max_mm':.25,'skin_strokes_total':len(groups),'closed_strokes_over_half_outside_prior_model':len(off_top),
         'closed_flags':[x[0] for x in off_top],
         'worst_candidates':sorted(rows,key=lambda x:x['unsupported_length_fraction']*x['length_mm'],reverse=True)[:30]}
 (ROOT/'validation'/output).write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
 print(json.dumps(result,indent=2))
 if off_top:
  selected=sorted(off_top,key=lambda x:x[0]['unsupported_length_fraction']*x[0]['length_mm'],reverse=True)[:4]
  import matplotlib
  matplotlib.use('Agg');import matplotlib.pyplot as plt
  from matplotlib.collections import LineCollection
  fig,axs=plt.subplots(1,len(selected),figsize=(12,3.6),dpi=160,squeeze=False)
  for ax,(row,p,segments) in zip(axs.flat,selected):
   ax.add_collection(LineCollection(segments,colors='#8993a1',linewidths=.7));ax.plot(p[:,0],p[:,1],color='#bb452d',lw=1.1)
   lo=p.min(axis=0)-3;hi=p.max(axis=0)+3;ax.set_xlim(lo[0],hi[0]);ax.set_ylim(lo[1],hi[1]);ax.set_aspect('equal');ax.grid(alpha=.15)
   ax.set_title(f"Z {row['z_mm']:.2f} mm | closed stroke\n{row['unsupported_length_fraction']*100:.0f}% outside prior model",fontsize=9);ax.set_xlabel('X (mm)')
  axs[0,0].set_ylabel('Y (mm)');fig.suptitle('Concentric skin needs a bridge-support check',fontsize=13)
  fig.text(.02,.02,'Red: current skin stroke. Gray: preceding model cross-section. This excludes bead width and neighboring deposited lines; it is a screening flag, not proof of failure.',fontsize=8)
  fig.subplots_adjust(bottom=.22,top=.79,wspace=.35);fig.savefig(ROOT/'engineering/figures'/figure)


if __name__=='__main__':
 if len(sys.argv)>1:sys.path.insert(0,sys.argv[1])
 import numpy as np
 run(*(sys.argv[2:]))
