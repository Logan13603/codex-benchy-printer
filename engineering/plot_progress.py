"""Plot checkpoint-008 analytical timing results; no physical measurements."""
import sys,json
from pathlib import Path
from path_model import ROOT
if len(sys.argv)>1:sys.path.insert(0,sys.argv[1])
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
base=json.loads((ROOT/'engineering/extrusion-dynamics-results.json').read_text(encoding='utf-8'))
new=json.loads((ROOT/'engineering/bridge-trial-results.json').read_text(encoding='utf-8'))
def row(d):return next(x for x in d['timing'] if x['extruder_instantaneous_corner_velocity_mm_s']==1 and x['mcr']==0)
b=row(base);n=new['trials'][0]['timing'][0]
vals=[b['seconds'],n['seconds'],n['cooling_floor_s'][0]['seconds'],n['cooling_floor_s'][2]['seconds']]
labels=['Previous path + extrusion check','Bridge-aware concentric skin','New path + 0.10 s layer floor','New path + 0.20 s layer floor']
fig,ax=plt.subplots(figsize=(11,4.4),dpi=170);fig.patch.set_facecolor('#f7f9fc');ax.set_facecolor('#f7f9fc')
y=list(range(4));ax.barh(y,vals,height=.53,color=['#748195','#377fba','#377fba','#c46b32'])
ax.invert_yaxis();ax.set_yticks(y,labels);ax.set_xlim(0,68);ax.set_xlabel('Calculated elapsed time (seconds)')
ax.axvline(55,color='#36517e',ls='--',lw=1.1);ax.axvline(60,color='#a83d33',ls=':',lw=1.3)
for i,v in enumerate(vals):ax.text(v+.5,i,f'{v:.2f}',va='center',fontsize=11,weight='bold')
ax.set_title('Faster toolpaths help, but physical performance remains unproven',loc='left',fontsize=13,pad=29)
ax.text(55,-.62,'55 s target',ha='right',fontsize=9,color='#36517e');ax.text(60,-.62,'60 s limit',ha='left',fontsize=9,color='#a83d33')
for side in ['top','right','left']:ax.spines[side].set_visible(False)
ax.grid(axis='x',alpha=.17);ax.set_axisbelow(True);ax.tick_params(axis='y',length=0)
fig.text(.025,.025,'All bars: V 2400 mm/s, A 2,000,000 mm/s², Q 300 mm³/s, SCV 500; E corner 1; MCR 0.\nCooling floors are assumed. Motor capability, shape accuracy and real extrusion/cooling remain unvalidated.',fontsize=9,color='#455164')
fig.subplots_adjust(left=.31,right=.965,bottom=.22,top=.76)
p=ROOT/'engineering/figures/toolpath-progress-008.png';fig.savefig(p);print(str(p.resolve()))
