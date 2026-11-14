from manim import *
from scenes.systems2x2.common import SystemsBase,ACCENT
class Cases(SystemsBase):
    def construct(self):
        self.heading('Сколько решений может иметь система?')
        xs=[-4.5,0,4.5]
        titles=['Одно решение','Нет решений','Бесконечно много']
        colors=[GREEN,RED,ManimColor(ACCENT)]
        systems=[r'\begin{cases}2x+y=5\\x-y=1\end{cases}',r'\begin{cases}2x+y=5\\4x+2y=11\end{cases}',r'\begin{cases}2x+y=5\\4x+2y=10\end{cases}']
        for i in range(3):
            title=Text(titles[i],font='DejaVu Sans',font_size=25,color=colors[i]);self.fit(title,width=4);title.move_to([xs[i],2.35,0])
            system=self.eq(systems[i],size=30,height=1.4,width=4).move_to([xs[i],1.1,0])
            condition=self.eq([r'D=-3\ne0','0=1','0=0'][i],size=34,color=colors[i],width=4).move_to([xs[i],-.55,0])
            answer=self.eq(['(2,1)',r'\varnothing',r'(x,y)=(t,5-2t)'][i],size=31,color=colors[i],width=4).move_to([xs[i],-1.55,0])
            self.check_frame(title,system,condition,answer)
            self.play(FadeIn(title),Write(system));self.play(Write(condition),Write(answer));self.wait(2)
        free=self.eq(r't\in\mathbb R',-2.4,size=28).move_to([4.5,-2.4,0]);self.play(Write(free))
        self.play(FadeIn(self.note('При D = 0 нельзя делить на D: исследуем совместность, например методом Гаусса.')));self.wait(4)
