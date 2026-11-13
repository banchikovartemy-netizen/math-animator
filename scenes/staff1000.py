from manim import *
from animation.components import ExplainedScene
from examples.staff1000_solution import COUNTS

COLORS=[YELLOW,BLUE,ORANGE,TEAL]
NAMES=['Учёные','Работники на ПК','Администраторы','Склад']
POSITIONS=[-4.7,-1.65,1.65,4.7]

class StaffAllocation(ExplainedScene):
    sample=False
    def label(self,value,x,y,size=25,color=WHITE):
        t=Text(value,font='DejaVu Sans',font_size=size,color=color)
        self.fit(t,width=3.0,height=.5);t.move_to([x,y,0]);self.check_frame(t);return t
    def construct(self):
        self.heading('Распределение 1000 человек')
        names=VGroup(*[self.label(n,x,2.35,23,c) for n,x,c in zip(NAMES,POSITIONS,COLORS)])
        original=COUNTS.copy();original[-1]=665
        labels=VGroup(*[self.label(str(n),x,1.75,34,c) for n,x,c in zip(original,POSITIONS,COLORS)])
        self.play(FadeIn(names),Write(labels),run_time=.7)
        left=-6;unit=.011
        def blocks(values):
            result=VGroup();offset=left
            for count,color in zip(values,COLORS):
                rect=Rectangle(width=count*unit,height=.65,stroke_width=0,fill_color=color,fill_opacity=.85)
                rect.move_to([offset+count*unit/2,.45,0]);offset+=count*unit;result.add(rect)
            return result
        initial=blocks(original)
        border=Rectangle(width=11,height=.75,color=WHITE,stroke_width=2).move_to([-.5,.45,0])
        limit=Line([5,-.1,0],[5,1.25,0],color=RED)
        limit_label=self.label('Лимит: 1000',4.95,1.32,20,RED)
        self.check_frame(initial,border,limit,limit_label)
        self.play(Create(border),FadeIn(initial),Create(limit),FadeIn(limit_label),run_time=.8)
        eq=self.formula('100+333+2+665=1100',-1)
        warning=self.label('Лишние 100 человек',0,-2,26,RED)
        self.fit(warning,width=12);warning.scale(1.4).move_to(DOWN*2)
        self.play(Write(eq),FadeIn(warning),run_time=.7);self.wait(2)
        calculation=self.formula('1000-100-333-2=565',-1)
        clarification=Text('По уточнению: меняем только число работников склада.',font='DejaVu Sans',font_size=25).move_to(DOWN*2.1)
        self.fit(clarification,width=12)
        self.play(ReplacementTransform(eq,calculation),ReplacementTransform(warning,clarification),run_time=.7)
        final=blocks(COUNTS)
        warehouse=self.label('565',POSITIONS[-1],1.75,34,TEAL)
        self.play(Transform(initial,final),ReplacementTransform(labels[-1],warehouse),FadeOut(limit),FadeOut(limit_label),run_time=1)
        self.wait(2)
        checked=self.formula('100+333+2+565=1000',-1)
        self.play(ReplacementTransform(calculation,checked),FadeOut(clarification),run_time=.7)
        percents=VGroup(*[self.label(p,x,1.15,25,c) for p,x,c in zip(['10%','33,3%','0,2%','56,5%'],POSITIONS,COLORS)])
        self.play(Write(percents),run_time=.7)
        # Russian prose avoids Cyrillic in LaTeX.
        rule=Text('Доля группы = число людей ÷ 1000 × 100%',font='DejaVu Sans',font_size=26).move_to(DOWN*2)
        self.fit(rule,width=12)
        self.play(FadeIn(rule),run_time=.5)
        note=Text('Каждый человек учтён в одной группе. Всего: 1000 человек, 100%.',font='DejaVu Sans',font_size=25)
        self.fit(note,width=12);note.move_to(DOWN*3.2)
        self.play(FadeIn(note),run_time=.5)
        self.wait(2 if self.sample else 5)

class StaffSample(StaffAllocation):
    sample=True
