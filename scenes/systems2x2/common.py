from manim import *
from animation.components import ExplainedScene,ACCENT
SYSTEM=r'\begin{cases}2x+y=5\\x-y=1\end{cases}'
class SystemsBase(ExplainedScene):
    def eq(self,tex,y=0,size=38,color=WHITE,width=12.1,height=1.15):
        m=MathTex(tex,font_size=size,color=color)
        self.fit(m,width=width,height=height);m.move_to(UP*y);self.check_frame(m);return m
    def note(self,value,y=-3.35,size=24):
        m=Text(value,font='DejaVu Sans',font_size=size)
        self.fit(m,width=12.1,height=.55);m.move_to(UP*y);self.check_frame(m);return m
    def change(self,old,tex,y=0,size=38,color=WHITE):
        new=self.eq(tex,y,size,color);self.play(TransformMatchingTex(old,new),run_time=.8);self.wait(1.4);return new
    def system(self,x=-4,y=1.8):
        m=self.eq(SYSTEM,size=37,height=1.5,width=4).move_to([x,y,0]);self.check_frame(m);return m
    def plot(self):
        ax=Axes(x_range=[-.5,4.5,1],y_range=[-2,6,1],x_length=7.2,y_length=4.5,axis_config={'font_size':20}).move_to(LEFT*2.5+DOWN*.2)
        ax.add_coordinates(font_size=20);labels=ax.get_axis_labels(x_label='x',y_label='y')
        first=ax.plot(lambda x:5-2*x,x_range=[0,3.5],color=BLUE,stroke_width=3)
        second=ax.plot(lambda x:x-1,x_range=[-.5,4.5],color=YELLOW,stroke_width=3)
        point=Dot(ax.c2p(2,1),color=ManimColor(ACCENT),radius=.085)
        guides=VGroup(ax.get_vertical_line(ax.c2p(2,1),color=ManimColor(ACCENT)),ax.get_horizontal_line(ax.c2p(2,1),color=ManimColor(ACCENT)))
        a=self.eq('y=5-2x',size=33,color=BLUE,width=4).move_to([4.25,1.75,0])
        b=self.eq('y=x-1',size=33,color=YELLOW,width=4).move_to([4.25,.7,0])
        answer=self.eq('(x,y)=(2,1)',size=34,color=ACCENT,width=4.5).move_to([4.25,-1,0])
        self.check_frame(ax,labels,first,second,point,guides,a,b,answer)
        return VGroup(ax,labels,first,second,point,guides,a,b,answer)
