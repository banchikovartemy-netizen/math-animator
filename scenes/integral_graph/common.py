from manim import *
from animation.components import ExplainedScene,ACCENT
import numpy as np

class IntegralBase(ExplainedScene):
    def title(self,value):return self.heading(value)
    def line(self,value,y=0,size=36,color=WHITE):
        m=MathTex(value,font_size=size,color=color)
        self.fit(m,width=12.1,height=.85);m.move_to(UP*y);self.check_frame(m);return m
    def note(self,value,y=-3.35,size=24):
        m=Text(value,font='DejaVu Sans',font_size=size)
        self.fit(m,width=12.1,height=.55);m.move_to(UP*y);self.check_frame(m);return m
    def plot(self):
        ax=Axes(x_range=[-4.5,4.5,1],y_range=[-6,6,2],x_length=7.2,y_length=4.35,
                axis_config={'include_tip':True,'font_size':20}).move_to(LEFT*2.5+DOWN*.25)
        ax.add_coordinates(font_size=19)
        labels=ax.get_axis_labels(x_label='x',y_label='F(x)')
        curve=ax.plot(lambda t:t**3/3-4*t,x_range=[-4,4],color=ManimColor(ACCENT),stroke_width=3)
        self.check_frame(ax,labels,curve)
        return ax,labels,curve
    def summary(self):
        ax,labels,curve=self.plot()
        top=self.line(r'F(x)=\frac{x^3}{3}-4x,\quad C=0',2.65,31)
        values=[(r'\max_{\mathrm{loc}}:\ (-2,\frac{16}{3})',YELLOW),
                (r'\min_{\mathrm{loc}}:\ (2,-\frac{16}{3})',BLUE),
                (r'\mathrm{inflection}:\ (0,0)',WHITE)]
        descriptions=VGroup(*[self.line(t,0,27,c).move_to([4.3,1.45-i*1.3,0]) for i,(t,c) in enumerate(values)])
        # Russian labels keep explanation accessible; formulas carry coordinates.
        descriptions[2].become(VGroup(Text('Перегиб:',font='DejaVu Sans',font_size=22),MathTex('(0,0)',font_size=28)).arrange(RIGHT,buff=.2).move_to([4.3,-1.15,0]))
        dots=VGroup(Dot(ax.c2p(-2,16/3),color=YELLOW),Dot(ax.c2p(2,-16/3),color=BLUE),Dot(ax.c2p(0,0),color=WHITE))
        guides=VGroup(ax.get_vertical_line(ax.c2p(-2,16/3),color=YELLOW),ax.get_vertical_line(ax.c2p(2,-16/3),color=BLUE))
        self.check_frame(descriptions,top,dots,guides)
        return VGroup(ax,labels,curve,top,descriptions,dots,guides)
