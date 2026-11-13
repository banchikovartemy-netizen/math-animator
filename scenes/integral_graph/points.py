from manim import *
from scenes.integral_graph.common import IntegralBase,ACCENT
class Points(IntegralBase):
    def construct(self):
        self.title('Считаем точки и строим график')
        ax,labels,curve=self.plot()
        self.play(Create(ax),Write(labels))
        substitutions=[(-4,-16/3,r'F(-4)=-\frac{64}{3}+16=-\frac{16}{3}'),
                       (-2,16/3,r'F(-2)=-\frac83+8=\frac{16}{3}'),
                       (0,0,r'F(0)=0-0=0'),
                       (2,-16/3,r'F(2)=\frac83-8=-\frac{16}{3}'),
                       (4,16/3,r'F(4)=\frac{64}{3}-16=\frac{16}{3}')]
        heading=self.line(r'F(x)=\frac{x^3}{3}-4x',2.65,32)
        self.play(Write(heading))
        current=None;table=VGroup()
        for i,(x,y,tex) in enumerate(substitutions):
            expr=MathTex(tex,font_size=26).move_to([4.15,1.9-i*.85,0])
            self.fit(expr,width=4.35,height=.65);self.check_frame(expr)
            dot=Dot(ax.c2p(x,y),color=YELLOW if x==-2 else BLUE if x==2 else WHITE)
            self.play(Write(expr),FadeIn(dot),run_time=.8);table.add(expr);self.wait(1.5)
        self.play(Create(curve),run_time=2)
        self.play(FadeIn(self.note('Кривая строится по формуле F(x); вычисленные точки проверяют её положение.')))
        self.wait(4)
