import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from pathlib import Path
# Prefer Times New Roman where installed; otherwise use a portable serif.
for font in Path('/System/Library/Fonts/Supplemental').glob('Times New Roman*.ttf'):
    font_manager.fontManager.addfont(str(font))
from matplotlib.patches import Rectangle, Circle
import json, pandas as pd
from pathlib import Path
base=Path(__file__).resolve().parents[1]; out=base/'figures'
s=json.loads((base/'examples/summary.json').read_text()); b=pd.read_csv(base/'examples/balance.csv')
plt.rcParams.update({'font.family':'serif','font.serif':['Times New Roman','Liberation Serif','DejaVu Serif'],'font.size':9,'svg.fonttype':'none','pdf.fonttype':42,'axes.linewidth':.6})
ink='#111111'; muted='#555555'; blue='#426d8b'; green='#557f74'; gold='#a78649'; gray='#c8cdd1'
fig=plt.figure(figsize=(12,6.1),facecolor='white')
fig.text(.045,.95,'Renal replacement therapy timing in acute kidney injury',fontsize=15,fontweight='bold',color=ink)


def panel(pos,letter,title,sub):
 ax=fig.add_axes(pos); ax.set(xlim=(0,100),ylim=(12,100)); ax.axis('off')
 ax.text(0,97,letter,fontsize=16,fontweight='bold',va='top',color=ink)
 ax.text(6,96,title,fontsize=11,fontweight='bold',va='top',color=ink)

 ax.plot([0,100],[87,87],color=gray,lw=.65)
 return ax

def box(ax,x,y,w,h,text,color=blue,fill='#f3f6f8',fs=9,dash=False):
 ax.add_patch(Rectangle((x,y),w,h,fc='white',ec='#111111',lw=1.0,ls='--' if dash else '-'))
 ax.text(x+w/2,y+h/2,text,ha='center',va='center',fontsize=fs,color=ink,linespacing=1.5)
def arrow(ax,a,z,c=muted,dash=False):
 ax.annotate('',xy=z,xytext=a,arrowprops=dict(arrowstyle='-|>',lw=.85,color='#111111',linestyle='--' if dash else '-',mutation_scale=9))
def person(ax,x,y,c=blue):
 ax.add_patch(Circle((x,y+5),1.1,fc=c,ec='none')); ax.plot([x,x],[y+3.5,y-1],c=c,lw=1.8)
 ax.plot([x-1.8,x,x+1.8],[y+1,y+3,y+1],c=c,lw=1.3); ax.plot([x-1.5,x,x+1.5],[y-4,y-1,y-4],c=c,lw=1.3)
A=panel([.045,.535,.435,.36],'a','Clinical question','Course project')
for xx in [4,9,14]: person(A,xx,66)
A.text(20,71,'Adults with incident stage 3 AKI',fontsize=10,fontweight='bold',color=ink)
A.text(20,62,'Early versus deferred initiation',fontsize=9,color=ink)
arrow(A,(50,56),(50,49))
box(A,7,28,37,20,'Early RRT')
box(A,57,28,37,20,'Deferred / no early RRT')
A.plot([25,75],[52,52],c=gray,lw=.8);arrow(A,(25,52),(25,49));arrow(A,(75,52),(75,49))
A.text(50,20,'Endpoint: 30-day mortality',ha='center',fontsize=9,color=ink)

B=panel([.535,.535,.42,.36],'b','Target trial timeline','Proposed extension')
B.plot([7,95],[62,62],c=ink,lw=1)
for x,label in [(28,'0'),(58,'24 h'),(92,'30 d')]:
 B.plot([x,x],[60,64],c=ink,lw=.8);B.text(x,67,label,ha='center',fontsize=9,color=ink)
B.text(28,77,'Stage 3 AKI onset',ha='center',fontsize=9,fontweight='bold',color=ink)
B.plot([7,27],[56,56],c=green,lw=3);B.text(17,45,'Pre-baseline\ncovariates',ha='center',fontsize=8.5,color=green)
B.plot([29,58],[56,56],c=gold,lw=3);B.text(44,45,'Treatment\nwindow',ha='center',fontsize=8.5,color=gold)
B.plot([59,92],[56,56],c=blue,lw=3);B.text(77,45,'Outcome\nfollow-up',ha='center',fontsize=8.5,color=blue)
box(B,0,19,28,14,'Align time zero',fill='white',fs=8,dash=True)
box(B,36,19,28,14,'Clone–censor',fill='white',fs=8,dash=True)
box(B,72,19,28,14,'Weight → estimate',fill='white',fs=8,dash=True)
arrow(B,(28,26),(36,26),dash=True);arrow(B,(64,26),(72,26),dash=True)

C=panel([.045,.105,.435,.405],'c','Analysis workflow','Course methods and public demo')
C.set_ylim(0,100)
C.text(0,75,'COURSE METHODS',fontsize=8,color=muted,fontweight='bold')
box(C,0,54,29,15,'Propensity score',fs=8.5)
box(C,37,54,29,15,'Weighted Cox',fs=8.5)
box(C,74,54,26,15,'Causal forest',fs=8.5)
arrow(C,(29,61),(37,61))
C.text(0,44,'SYNTHETIC DEMO',fontsize=8,color=green,fontweight='bold')
box(C,0,17,27,20,'Simulate X, A, T',green,'#f1f6f3',8.5)
box(C,36,17,30,20,'IPW / AIPW\nCox / causal forest',green,'#f1f6f3',8)
box(C,75,17,25,20,'Diagnostics\nEffect estimates',green,'#f1f6f3',8.3)
arrow(C,(27,27),(36,27));arrow(C,(66,27),(75,27))
C.text(0,5,'n = 4,000  ·  Baseline intervention  ·  Fully synthetic',fontsize=8.1,color=muted,linespacing=1.5)
D=panel([.535,.105,.42,.405],'d','Diagnostics and effects','Synthetic results')
D.set_ylim(0,100)
# real plots inset in panel coordinates
p=D.inset_axes([.11,.29,.34,.43]);
y=list(range(4));p.scatter(abs(b.smd_before),y,c=gold,s=20,label='Before');p.scatter(abs(b.smd_after),y,c=green,s=20,label='After')
for i,r in b.iterrows(): p.plot([abs(r.smd_before),abs(r.smd_after)],[i,i],color=gray,lw=.8,zorder=0)
p.axvline(.1,color=gray,ls='--',lw=.8);p.set_yticks(y,['Age','Severity','Renal marker','Comorbidity'],fontsize=7);p.invert_yaxis();p.set_xlim(-.03,.75);p.set_xticks([0,.3,.6]);p.tick_params(labelsize=7,length=2);p.set_xlabel('Absolute SMD',fontsize=7)
p.set_title('Covariate balance',fontsize=9,loc='left',pad=10)
p.spines[['top','right','left']].set_visible(False);p.legend(loc='upper center',bbox_to_anchor=(.5,-.27),ncol=2,fontsize=7,frameon=False,handletextpad=.3,columnspacing=.9)
q=D.inset_axes([.64,.29,.35,.43]);
vals=[s['unadjusted_risk_difference'],s['ipw_risk_difference'],s['aipw_risk_difference']]
q.scatter([v*100 for v in vals],[2,1,0],s=23,c=[gold,blue,green],zorder=3)
lo,hi=s['aipw_ci95'];q.plot([lo*100,hi*100],[0,0],c=green,lw=1.3)
q.axvline(0,c=gray,lw=.8);q.axvline(s['oracle_mean_risk_difference']*100,c=green,lw=.8,ls='--')
q.set_yticks([2,1,0],['Unadjusted','IPW','AIPW'],fontsize=7);q.set_ylim(-.65,2.65);q.set_xlim(-12,12);q.set_xticks([-10,0,10]);q.tick_params(labelsize=7,length=2);q.set_xlabel('Risk difference (pp)',fontsize=7)
q.set_title('30-day effect estimates',fontsize=9,loc='left',pad=10);q.spines[['top','right','left']].set_visible(False)
D.text(64,13,'Dashed: oracle  ·  Bar: 95% CI',fontsize=7.1,color=muted,linespacing=1.5)

fig.text(.045,.048,'Figure 1. Study overview.',fontsize=9,fontweight='bold',color=ink)
fig.text(.045,.025,'Dashed boxes: proposed methods. Panel d: synthetic demonstration, not clinical RRT effects.',fontsize=8,color=muted)
for ext in ['png','svg','pdf']: fig.savefig(out/f'workflow.{ext}',dpi=220,facecolor='white')
