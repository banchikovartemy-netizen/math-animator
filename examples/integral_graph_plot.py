"""Standalone, exportable mathematical figure; same reviewed symbolic data."""
import argparse
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from examples.integral_graph_solution import F,x,POINTS,build_solution
from math_engine.checks import require_passed


def export(path):
    require_passed(build_solution().checks)
    plt.rcParams.update({'font.family':'DejaVu Sans','text.color':'white','axes.labelcolor':'white','xtick.color':'white','ytick.color':'white','font.size':12})
    fig,(ax,notes)=plt.subplots(1,2,figsize=(16,9),gridspec_kw={'width_ratios':[1.1,1]},facecolor='black')
    for a in (ax,notes):a.set_facecolor('black')
    t=np.linspace(-4,4,801)
    ax.plot(t,t**3/3-4*t,color='#64d8cb',linewidth=2.5,label=r'$F(x)=x^3/3-4x$')
    ax.axhline(0,color='white',linewidth=.8);ax.axvline(0,color='white',linewidth=.8)
    for value,color,label in [(-2,'#ffff00',r'$(-2,16/3)$'),(2,'#58c4dd',r'$(2,-16/3)$')]:
        y=float(F.subs(x,value));ax.scatter([value],[y],color=color,s=70,zorder=5)
        ax.plot([value,value],[0,y],linestyle='--',color=color,alpha=.6)
        ax.annotate(label,(value,y),xytext=(10,14 if value<0 else -25),textcoords='offset points',color=color,fontsize=14)
    ax.scatter([0],[0],color='white',s=40,zorder=5)
    ax.scatter([-2*np.sqrt(3),2*np.sqrt(3)],[0,0],color='orange',s=45,zorder=5)
    ax.set(xlim=(-4.3,4.3),ylim=(-6.6,6.6),xlabel='x',ylabel='F(x)')
    ax.grid(alpha=.2,color='gray')
    for spine in ax.spines.values():spine.set_color('gray')
    ax.legend(facecolor='black',edgecolor='gray',labelcolor='white',loc='upper right')
    notes.axis('off')
    blocks=[('Интеграл и выбранная первообразная',r'$\int(x^2-4)\,dx=\frac{x^3}{3}-4x+C;\quad C=0$','white'),
            ('Критические точки',r"$F'(x)=x^2-4=0\Rightarrow x=\pm2$",'white'),
            ('Локальный максимум',r"$F''(-2)=-4<0;\quad F(-2)=-8/3+8=16/3$",'#ffff00'),
            ('Локальный минимум',r"$F''(2)=4>0;\quad F(2)=8/3-8=-16/3$",'#58c4dd'),
            ('Перегиб',r"$F''(x)=2x=0\Rightarrow x=0;\quad F(0)=0$",'white'),
            ('Нули функции',r'$x(x^2-12)/3=0\Rightarrow x=0,\ \pm2\sqrt{3}$','orange')]
    for i,(label,formula,color) in enumerate(blocks):
        y=.96-i*.15;notes.text(0,y,label,fontsize=13,color=color,transform=notes.transAxes)
        notes.text(0,y-.065,formula,fontsize=14,color=color,transform=notes.transAxes)
    fig.suptitle('Интеграл, график и расчёт характерных точек',fontsize=21,color='white',y=.98)
    fig.text(.05,.035,'Область определения: ℝ. Рост при x < −2 и x > 2; убывание при −2 < x < 2. Все значения проверены SymPy.',color='white',fontsize=12)
    fig.subplots_adjust(left=.06,right=.98,top=.9,bottom=.12,wspace=.25)
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    fig.savefig(path,dpi=160,facecolor='black');plt.close(fig)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);export(p.parse_args().output)
