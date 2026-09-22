"""Independent Gaussian integration check of sampled PA position convolution."""
import sys,json,math
from path_model import ROOT,parse
import extrusion_dynamics as ed


def exact_pa_at(t,st,pa,phase,last_e):
 starts,ends,ep,ev,ea,roles,dep=phase;h=st/2
 knots=[t-h,t,t+h]
 lo=max(0,int(np.searchsorted(ends,t-h,side='right')))
 hi=min(len(starts),int(np.searchsorted(starts,t+h,side='left')))
 knots+=list(starts[lo:hi]);knots+=list(ends[lo:hi])
 knots=sorted(set(x for x in knots if t-h<=x<=t+h))
 result=0.;nodes,weights=np.polynomial.legendre.leggauss(3)
 # Quadratic phase position times linear triangle is cubic: 3-point Gauss
 # quadrature is exact within each phase/kernel half, independent of sampling.
 for a,b in zip(knots[:-1],knots[1:]):
  x=(a+b)/2+(b-a)/2*nodes
  i=np.clip(np.searchsorted(ends,x,side='right'),0,len(ends)-1);u=x-starts[i]
  p=ep[i]+ev[i]*u+.5*ea[i]*u*u+pa*(ev[i]+ea[i]*u)*dep[i]
  p[x<0]=ep[0];p[x>ends[-1]]=last_e
  result+=(b-a)/2*np.sum(weights*p*(h-np.abs(x-t))/h**2)
 return result


def main():
 raw=parse(ROOT/'slicing/cura-travel-study/concentric-skin/analysis.gcode');planned=ed.plan(raw)
 phase=ed.phases(planned);starts,ends,ep,ev,ea,roles,dep=phase
 dt=.000025;t=np.arange(-.05,ends[-1]+.05,dt);i=np.clip(np.searchsorted(ends,t,side='right'),0,len(ends)-1);u=t-starts[i]
 e=ep[i]+ev[i]*u+.5*ea[i]*u*u;v=ev[i]+ea[i]*u
 e[t<0]=ep[0];e[t>ends[-1]]=planned[-1].end_pos[3];v[(t<0)|(t>ends[-1])]=0.
 rows=[]
 for st in (.04,.01,.004,.001):
  pa=.04;actual=ed.convolve(e+pa*v*dep[i],ed.triangular_kernel(st,dt))
  vel=np.gradient(actual,dt);worst=int(np.argmax(np.abs(vel)))
  ix=sorted(set(list(np.linspace(0,len(t)-1,51,dtype=int))+list(range(worst-3,worst+4))))
  errors=[abs(actual[j]-exact_pa_at(t[j],st,pa,phase,planned[-1].end_pos[3])) for j in ix]
  assert max(errors)<.002,(st,max(errors))
  rows.append({'smooth_time_s':st,'pa_s':pa,'dt_s':dt,'points_checked':len(ix),'max_abs_position_error_mm':max(errors)})
 result={'status':'Independent piecewise-polynomial Gaussian integration oracle; not physical validation','checks':rows,
         'method':'Each trapezoid and triangle-center boundary splits the integral; 3-point Gauss exactly integrates each cubic piece. Compare dt25us convolution including max-speed neighborhood and rest tails.'}
 (ROOT/'validation/extrusion-oracle.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
 print(json.dumps(result,indent=2))


if __name__=='__main__':
 if len(sys.argv)>1:sys.path.insert(0,sys.argv[1])
 import numpy as np
 ed.np=np;main()
