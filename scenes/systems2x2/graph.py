from manim import *
from scenes.systems2x2.common import SystemsBase,ACCENT
class Graphical(SystemsBase):
    def construct(self):
        self.heading('3. Графический метод')
        g=self.plot();ax,labels,first,second,point,guides,a,b,answer=g
        self.play(Create(ax),Write(labels))
        self.play(Write(a),Create(first),run_time=1.5)
        p1=VGroup(Dot(ax.c2p(0,5),color=BLUE),Dot(ax.c2p(2,1),color=BLUE))
        note=self.note('Первая прямая: точки (0,5) и (2,1).')
        calc1=self.eq(r'x=0:\ y=5;\quad x=2:\ y=5-4=1',size=25,width=4.5).move_to([4.25,.55,0])
        self.play(FadeIn(p1),FadeIn(note),Write(calc1));self.wait(2)
        self.play(FadeOut(calc1),run_time=.4)
        self.play(Write(b),Create(second),run_time=1.5)
        p2=Dot(ax.c2p(0,-1),color=YELLOW)
        new=self.note('Вторая прямая: точки (0,−1) и (2,1). Общая точка — решение.')
        calc2=self.eq(r'x=0:\ y=-1;\quad x=2:\ y=2-1=1',size=25,width=4.5).move_to([4.25,-.25,0])
        self.play(FadeIn(p2),ReplacementTransform(note,new),Write(calc2));self.wait(2)
        self.play(FadeOut(calc2),run_time=.4)
        self.play(Create(guides),FadeIn(point),Write(answer));self.wait(3)
        final=self.note('График показывает пересечение; точность подтверждаем подстановкой.')
        self.play(ReplacementTransform(new,final));self.wait(3)
class SystemsSample(SystemsBase):
    def construct(self):
        self.heading('Быстрая проверка: пересечение прямых')
        self.play(FadeIn(self.plot()),run_time=.6)
        self.play(FadeIn(self.note('2·2 + 1 = 5;  2 − 1 = 1.')),run_time=.4);self.wait(2)
