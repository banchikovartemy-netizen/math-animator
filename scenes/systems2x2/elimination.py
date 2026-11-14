from manim import *
from scenes.systems2x2.common import SystemsBase,ACCENT
class Elimination(SystemsBase):
    def construct(self):
        self.heading('2. Метод сложения')
        a=self.eq(r'2x+{{y}}=5',2.1)
        b=self.eq(r'x{{-y}}=1',1.05)
        a.set_color_by_tex('y',YELLOW);b.set_color_by_tex('-y',YELLOW)
        self.play(Write(a),Write(b));self.play(Indicate(a.get_part_by_tex('y')),Indicate(b.get_part_by_tex('-y')))
        note=self.note('Коэффициенты при y противоположны: складываем уравнения.')
        self.play(FadeIn(note))
        current=self.eq('(2x+y)+(x-y)=5+1',-.2)
        self.play(Write(current));self.wait(2)
        for tex in ['3x=6','x=2']:current=self.change(current,tex,-.2,color=ACCENT)
        back=self.eq('x-y=1\quad\Rightarrow\quad 2-y=1\quad\Rightarrow\quad y=1',-1.55,size=34)
        self.play(Write(back));self.wait(3)
        self.play(Write(self.eq('(x,y)=(2,1)',-2.45,color=YELLOW)));self.wait(3)
