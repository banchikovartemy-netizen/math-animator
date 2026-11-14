from manim import *
from scenes.systems2x2.common import SystemsBase,ACCENT
class Cramer(SystemsBase):
    def construct(self):
        self.heading('4. Формулы Крамера')
        data=[[[2,1],[1,-1]],[[5,1],[1,-1]],[[2,5],[1,1]]]
        matrices=[Matrix(d,element_to_mobject_config={'font_size':34},left_bracket='|',right_bracket='|').scale_to_fit_height(1.5).move_to([x,1.2,0]) for d,x in zip(data,[-4.4,0,4.4])]
        labels=VGroup(*[self.eq(t,2.4,size=35,width=3).move_to([x,2.4,0]) for t,x in zip(['D','D_x','D_y'],[-4.4,0,4.4])])
        self.play(Write(matrices[0]),Write(labels[0]))
        expressions=[r'2(-1)-1\cdot1=-3',r'5(-1)-1\cdot1=-6',r'2\cdot1-5\cdot1=-3']
        for i in range(3):
            if i:
                self.play(TransformFromCopy(matrices[0],matrices[i]),Write(labels[i]))
                box=SurroundingRectangle(matrices[i].get_columns()[i-1],color=YELLOW,buff=.08)
                self.play(Create(box))
            expr=self.eq(expressions[i],-.25,size=28,width=3.9).move_to([[-4.4,0,4.4][i],-.25,0])
            self.play(Write(expr));self.wait(2)
        note=self.note('В Dx заменяем первый столбец на (5,1), в Dy — второй.')
        self.play(FadeIn(note))
        ratios=self.eq(r'x=\frac{D_x}{D}=\frac{-6}{-3}=2,\qquad y=\frac{D_y}{D}=\frac{-3}{-3}=1',-1.6,size=36)
        self.play(Write(ratios));self.wait(3)
        condition=self.eq(r'D=-3\ne0',-2.6,size=34,color=ACCENT)
        self.play(Write(condition));self.wait(3)
