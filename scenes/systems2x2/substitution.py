from manim import *
from scenes.systems2x2.common import SystemsBase,ACCENT
class Substitution(SystemsBase):
    def construct(self):
        title=self.heading('Линейная система 2 × 2: шесть методов')
        system=self.system(-3.6,1.9)
        goal=self.note('Одна система — один ответ. Сравним шесть способов его получить.')
        self.play(Write(system),FadeIn(goal));self.wait(3)
        newtitle=self.note('1. Метод подстановки',y=3.45,size=34)
        self.play(ReplacementTransform(title,newtitle),FadeOut(goal))
        expressed=self.eq('x=y+1',2,size=39,color=ACCENT).move_to([3.2,2,0])
        self.play(TransformFromCopy(system,expressed),run_time=.9)
        self.play(FadeIn(self.note('Из второго уравнения выражаем x и подставляем в первое.')))
        current=self.eq(r'2\underbrace{(y+1)}_{x}+y=5',.35)
        self.play(Write(current));self.wait(2)
        for tex in ['3y+2=5','3y=3','y=1']:current=self.change(current,tex,.35)
        back=self.eq('x=y+1=1+1=2',-1.2,color=ACCENT)
        self.play(Write(back));self.wait(2)
        result=self.eq('(x,y)=(2,1)',-2.25,color=YELLOW)
        self.play(Write(result));self.wait(3)
