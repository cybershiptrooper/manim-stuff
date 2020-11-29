#!usr/bin/env python3
from manimlib.imports import *
import numpy as np
class Video1(GraphScene):
    global N
    N = 4
    CONFIG = {
        "axes_color" : BLUE,
        "y_tick_frequency" : 0.5,
        "x_tick_frequency" : 1,
        "x_axis_width": 5,
        "y_axis_width": 5,
        # "graph_origin":  2*DOWN,
        # "x_min": -N,
        # "x_max": N,
        # "y_min": -0.5,
        # "y_max": 2,
        # "y_labeled_nums" : [0,0.5,1,1.5],
        # "y_bottom_tick" : 0,
        # "x_labeled_nums" : list(np.arange(-N,N+0.5,0.5))
    };
    
    
    def construct(self):
        title = TextMobject("Part 1- DFT as samples of DTFT")
        self.play(Write(title))
        self.wait()
        self.play(FadeOut(title));
        self.wait();
        text = TextMobject("Consider a rectangular pulse-")
        math = TexMobject("x_{N}[n] = "
        	"\\begin{cases} 1,& \\text{if } 0 \\leq n < N\\\\ 0  & \\text{otherwise} \\end{cases}"
        	)
        VGroup(text, math).arrange(DOWN)
        self.play(
            Write(text),
            FadeInFrom(math, UP),
        )
        self.wait()
        text2 = TextMobject("Let us visualise $x_{}$".format(N))
        math_new = TexMobject("x_{N}[n] = "
        	"\\begin{cases} 1,& \\text{if } 0 \\leq n <" +str(N/2)+"\\\\ 0  & \\text{otherwise} \\end{cases}"
        	)
        math_new.to_corner(UP + LEFT)
        self.play(
        	Transform(math, math_new),
        	Transform(text, text2)
        	)
        self.wait()
        self.play(
        	FadeOut(text2),
        	FadeOut(text),
        )
        self.drawrect();
        self.play(
        	FadeOut(math_new),
        	FadeOut(math),
        	)
        text = TextMobject("The fourier transform of this function is")
        string = "X(w) = \\frac{1-exp(-jw)}{1-exp(-jw/"+str(N)+")}"
        fourier = TexMobject(string)
        VGroup(text, fourier).arrange(DOWN)
        self.play(Write(text))
        self.wait()
        self.play(FadeInFrom(fourier, UP))
        self.wait()
        self.play(
            FadeOut(text),
            FadeOut(fourier)
        )
        text = TextMobject("Now we will sample $|X(w)|$\n"
        	"at $w=\\frac{2\\pi k}{"+str(N/2)+"}$")
        text2 = TextMobject("where $k\\in {0,1,.."+str(N-1)+"}$")

        VGroup(text, text2).arrange(DOWN)
        self.play(Write(text),)
        self.wait()
        self.play(Transform(text, text2))
        self.wait()
        self.play(FadeOut(text2))
        self.play(FadeOut(text))
        self.drawsinc()
        self.wait()

    def drawrect(self):
        self.setup_axespt1()
        func_graph=self.get_graph(self.rect, YELLOW, xmin = -10, xmax = 10)
        #vert_line = self.get_vertical_line_to_graph(TAU,func_graph,color=YELLOW)
        self.play(Write(func_graph))
        #self.play(ShowCreation(vert_line))
        for i in range(0, N):
        	if(not self.rect(i)): continue
        	point = Dot(self.coords_to_point(i,1))
        	vert_line = self.get_vertical_line_to_graph(i,func_graph,color=YELLOW)
        	self.play(ShowCreation(vert_line))
        	self.add(point)
        self.play(FadeOut(func_graph))
        self.wait(2)
        self.clear()

    def setup_axespt1(self):
        # GraphScene.setup_axes(self, animate = True)
        self.graph_origin = 2 * DOWN 
        #self.x_axis.label_direction = UP
        # self.y_axis.label_direction = LEFT*1.5
        self.x_min = -10
        self.x_max = 10
        self.y_max = 2
        self.y_min = -0.5
        self.x_axis_label = "$t$"
        self.y_axis_label = "$y$"
        init_val_x = -10
        step_x = 2
        end_val_x = 10
        values_decimal_x=list(np.arange(init_val_x,end_val_x+step_x,step_x))
        list_x=[*["%.1f"%i for i in values_decimal_x]]
        values_x = [
            (i,j)
            for i,j in zip(values_decimal_x,list_x)
        ]
        self.x_axis_labels = VGroup()
        GraphScene.setup_axes(self)
        for x_val, x_tex in values_x:
            tex = TexMobject(x_tex)
            tex.scale(0.4)
            tex.next_to(self.coords_to_point(x_val, 0), DOWN)
            self.x_axis_labels.add(tex)
        
        self.play(
            Write(self.x_axis_labels),
            Write(self.x_axis),
            Write(self.y_axis)
        )
	
    def drawsinc(self):
    	self.setup_axespt2()
    	func_graph= self.get_graph(self.sinc, YELLOW, xmin = -1.0, xmax = 1.0)
    	self.play(ShowCreation(func_graph))
    	for i in range(0, N):
    		point = Dot(self.coords_to_point(2*PI*i/N,self.sinc(2*PI*i/N)))
    		vert_line = self.get_vertical_line_to_graph(2*PI*i/N,func_graph)
    		self.play(ShowCreation(vert_line))
    		self.add(point)
    	for i in range(0, N):
    		y = self.sinc(2*PI*i/N) 
    		y = str(N) if y == N else str(0);
    		string = "sample \\#"+str(i+1)+"="+y
    		text=TextMobject(string)
    		text.move_to(2*RIGHT+3*(2*i/N-1)*DOWN)
    		text.arrange(RIGHT, center=False, aligned_edge=LEFT) 
    		text.scale(0.7)
    		self.play(Write(text))
    	self.play(FadeOut(func_graph))
    	self.wait(2)
    	self.clear()

    def setup_axespt2(self):
        self.graph_origin = 2.5 * DOWN + 5 * LEFT
        #self.x_axis.label_direction = UP
        # self.y_axis.label_direction = LEFT*1.5
        self.y_axis.add_numbers(*[N])
        self.x_min = 0
        self.x_max = 2*PI
        self.x_leftmost_tick = 0;
        self.y_max = N+1
        self.y_min = -1
        self.x_axis_label = "$w$"
        self.y_axis_label = "$|X(w)|$"
        # self.x_label.move_to(0.5*LEFT)
        init_val_x = 0
        step_x = 1
        end_val_x = 2*PI
        values_decimal_x=list(np.arange(init_val_x,end_val_x+step_x,step_x))
        list_x=[*["%.1f"%i for i in values_decimal_x]]
        values_x = [
            (i,j)
            for i,j in zip(values_decimal_x,list_x)
        ]
        self.x_axis_labels = VGroup()
        GraphScene.setup_axes(self, animate = True)
        for x_val, x_tex in values_x:
            tex = TexMobject(x_tex)
            tex.scale(0.7)
            tex.next_to(self.coords_to_point(x_val, 0), DOWN)
            self.x_axis_labels.add(tex)
        self.play(
            Write(self.x_axis_labels),
        )

    #functions to graph
    def sinc(self, f):
        if f<=2*PI and f>PI:
        	f = f-2*PI
        if(f == 0): return N
        return abs(2*np.sin(N*f/2)/f)


    def rect(self, x):
        return float(x<N and x >= 0)


class Video2(Scene):
    def construct(self):
        title = TextMobject("Part 1")
        self.play(Write(title))
        self.wait()
        self.play(FadeOut(title));
        self.wait();


#todo:
#-1,1 -> 0,2pi
# 0,5