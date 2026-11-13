"""All 25 dot products, all 125 multiplications and all 100 additions."""
from manim import *
from animation.components import ExplainedScene, ACCENT
from examples.matrix5_solution import A, B, EXPECTED, cell_work, signed

ROW = YELLOW
COLUMN = ManimColor(ACCENT)

class DetailedMatrix5(ExplainedScene):
    rows = range(5)
    columns = range(5)
    intro = True
    intro_only = False
    outro = True

    def numeric(self, value, y, size=38, color=WHITE):
        # Numeric arithmetic needs no new LaTeX process for every pair of integers.
        obj = Text(value.replace('-', '−'), font='DejaVu Serif', font_size=size, color=color)
        self.fit(obj, width=12.2, height=.65);obj.move_to(UP*y);self.check_frame(obj)
        return obj

    def text(self, value, size=25):
        return Text(value, font='DejaVu Sans', font_size=size)

    def math(self, value, y, size=34, color=WHITE):
        obj = MathTex(value, font_size=size, color=color)
        self.fit(obj, width=12.3, height=.68)
        obj.move_to(UP*y)
        self.check_frame(obj)
        return obj

    def construct(self):
        title = self.text('Умножение матриц 5 × 5', 34).move_to(UP*3.55)
        subtitle = self.text('Каждый элемент: строка A × столбец B', 23).move_to(UP*2.98)
        if self.intro:self.play(Write(title), FadeIn(subtitle), run_time=1.1)
        else:self.add(title,subtitle)
        # Equal column spacing, fixed positions, and identical scales prevent layout drift.
        a = Matrix(A, h_buff=.82, v_buff=.62, element_to_mobject_config={'font_size':30})
        b = Matrix(B, h_buff=.82, v_buff=.62, element_to_mobject_config={'font_size':30})
        c = Matrix(EXPECTED, h_buff=.94, v_buff=.62, element_to_mobject_config={'font_size':30})
        a.scale_to_fit_height(2.15).move_to(LEFT*4.6+UP*1.45)
        b.scale_to_fit_height(2.15).move_to(LEFT*.15+UP*1.45)
        c.scale_to_fit_height(2.15).move_to(RIGHT*4.45+UP*1.45)
        labels = VGroup(*[MathTex(s, font_size=31, color=col).move_to([x,2.72,0])
                          for s,x,col in [('A',-4.6,ROW),('B',-.15,COLUMN),('C=AB',4.45,WHITE)]])
        symbols = VGroup(MathTex(r'\times',font_size=30).move_to([-2.4,1.45,0]),
                         MathTex('=',font_size=30).move_to([2.1,1.45,0]))
        pending = VGroup(*[MathTex(r'\cdot',font_size=25,color=GRAY).move_to(e) for e in c.get_entries()])
        self.check_frame(a,b,c,labels,symbols,pending)
        if self.intro:
            self.play(Write(a),Write(b),Write(labels),Write(symbols),Write(c.get_brackets()),FadeIn(pending),run_time=2)
            rule=self.math(r'(5\times5)\,(5\times5)\;\longrightarrow\;5\times5',-.25)
            instruction=self.text('Внутренние размеры совпадают: умножение определено.',24).move_to(DOWN*1.2)
            self.play(Write(rule),FadeIn(instruction))
            self.wait(3)
            general=self.math(r'c_{ij}=a_{i1}b_{1j}+a_{i2}b_{2j}+a_{i3}b_{3j}+a_{i4}b_{4j}+a_{i5}b_{5j}',-.25)
            self.play(ReplacementTransform(rule,general),FadeOut(instruction))
            note=VGroup(self.text('В каждой ячейке: 5 умножений, затем 4 сложения.',24).move_to(DOWN*1.25),
                        self.text('sₖ — сумма первых k произведений.',24).move_to(DOWN*2))
            self.play(FadeIn(note));self.wait(4)
            self.play(FadeOut(note),FadeOut(general))
        else:
            self.add(a,b,labels,symbols,c.get_brackets(),pending)
            for index in range(5*min(self.rows)):
                self.remove(pending[index]);self.add(c.get_entries()[index])
        if self.intro_only:return

        progress=self.text(f'Строка {min(self.rows)+1} из 5',22).move_to(DOWN*3.55)
        if self.intro:self.play(FadeIn(progress))
        else:self.add(progress)
        completed = VGroup()
        for i in self.rows:
            for j in self.columns:
                cell_index=5*i+j
                row_box=SurroundingRectangle(a.get_rows()[i],color=ROW,buff=.07,stroke_width=2)
                col_box=SurroundingRectangle(b.get_columns()[j],color=COLUMN,buff=.07,stroke_width=2)
                destination=SurroundingRectangle(pending[cell_index],color=WHITE,buff=.12,stroke_width=2)
                caption=self.text(f'Элемент {i+1},{j+1}: строка {i+1} × столбец {j+1}',24).move_to(DOWN*.12)
                new_progress=self.text(f'Строка {i+1} из 5  •  Элемент {cell_index+1} из 25',22).move_to(DOWN*3.55)
                self.play(Create(row_box),Create(col_box),Create(destination),FadeIn(caption),ReplacementTransform(progress,new_progress),run_time=.55)
                progress=new_progress
                # Reserve all five slots before revealing anything, avoiding equation jumps.
                expansion = MathTex(f'c_{{{i+1}{j+1}}}=',
                    *[('+' if k else '')+f'{signed(A[i][k])}\\cdot{signed(B[k][j])}' for k in range(5)],font_size=34)
                self.fit(expansion,width=12.2,height=.58);expansion.move_to(DOWN*.85)
                self.check_frame(expansion)
                self.play(Write(expansion[0]),run_time=.3)
                products,totals=cell_work(i,j)
                running=None
                multiplication=None
                for k in range(5):
                    pair=VGroup(a.get_entries()[5*i+k],b.get_entries()[5*k+j])
                    new_multiplication=self.numeric(f'{signed(A[i][k])} · {signed(B[k][j])} = {products[k]}',-1.63,size=36,color=COLUMN)
                    subscript=str(k+1).translate(str.maketrans('12345','₁₂₃₄₅'))
                    new_sum=self.numeric(f's{subscript} = {products[k]}' if k==0 else f's{subscript} = {signed(totals[k-1])} + {signed(products[k])} = {totals[k]}',-2.45,size=35,color=ROW)
                    animations=[FadeIn(new_multiplication) if multiplication is None else ReplacementTransform(multiplication,new_multiplication),
                                FadeIn(new_sum) if running is None else ReplacementTransform(running,new_sum)]
                    self.play(*animations,Indicate(pair[0],color=ROW,scale_factor=1.18),
                              Indicate(pair[1],color=COLUMN,scale_factor=1.18),Write(expansion[k+1]),run_time=1.1)
                    multiplication,running=new_multiplication,new_sum
                    self.wait(1.1 if cell_index else 1.8)
                result=self.math(f'c_{{{i+1}{j+1}}}={totals[-1]}',-2.45,size=40,color=COLUMN)
                self.play(ReplacementTransform(running,result),run_time=.4)
                target=c.get_entries()[cell_index]
                self.play(FadeOut(pending[cell_index]),TransformFromCopy(result,target),run_time=.7)
                completed.add(target)
                self.wait(.9)
                self.play(*[FadeOut(obj) for obj in (row_box,col_box,destination,caption,expansion,multiplication,result)],run_time=.4)
            if i<4:
                self.play(Indicate(c.get_rows()[i],color=COLUMN,scale_factor=1.04),run_time=.6)
                self.wait(.8)

        if not self.outro:return
        self.play(FadeOut(progress),FadeOut(a),FadeOut(b),FadeOut(symbols),FadeOut(labels),run_time=.8)
        # The full answer occupies the centre only after all arithmetic is complete.
        self.clear()
        self.add(title)
        final=Matrix(EXPECTED,h_buff=1.15,v_buff=.7,element_to_mobject_config={'font_size':38})
        final.scale_to_fit_height(3.6).move_to(UP*.35)
        self.play(FadeOut(c.get_brackets()),FadeOut(completed),FadeIn(final),run_time=1)
        answer=self.math(r'C=AB',2.65,size=39,color=COLUMN)
        self.play(Write(answer))
        checks=self.text('Все 25 элементов проверены независимо через SymPy.',25).move_to(DOWN*2.2)
        counts=self.text('Вычислено: 125 произведений и 100 сложений.',25).move_to(DOWN*2.85)
        self.play(FadeIn(checks),FadeIn(counts))
        self.wait(7)
