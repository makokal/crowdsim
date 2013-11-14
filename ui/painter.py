from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Line, Rectangle
from kivy.uix.floatlayout import FloatLayout

from random import random

class MyPaintWidget(Widget):

    def on_touch_down(self, touch):
        with self.canvas:
            Color(1, 1, 0)
            d = 30.
            Ellipse(pos=(touch.x - d / 2, touch.y - d / 2), size=(d, d))
            touch.ud['line'] = Line(points=(touch.x, touch.y))

    def on_touch_move(self, touch):
        touch.ud['line'].points += [touch.x, touch.y]


        

class Cell(Widget):
    def __init__(self, px, py):
        super(Cell, self).__init__()
        self.px, self.py = px, py
        with self.canvas:
            Color(1, 0.2, 0,2)
            Rectangle(pos=(self.px, self.py), size=(40,40))


class Ball(Widget):
    """docstring for Ball"""
    def __init__(self, **kwargs):
        super(Ball, self).__init__(**kwargs)
        self.pos = (200, 200)
        with self.canvas:
            Color(1, 1, 0.0)
            self.circle = Ellipse(pos=self.pos, size=(50,50))

    def on_pos(self, obj, new_pos):
        self.pos = 

    def move(self, np):
        self.pos = np

        


class Field(Widget):
    cell_size = 40
    grid_size = 600, 400


    def __init__(self, **kwargs):
        super(Field, self).__init__(**kwargs)

        self.pos = (100, 100)
        self.size = (600, 600)

        with self.canvas:
            Color(0.1, 0.1, 0.1)
            Rectangle(pos=self.pos, size=self.size)

        print self.height, self.width, self.pos, self.size
        self.draw_grid()

    def draw_grid(self):
        with self.canvas:
            for row in xrange(self.pos[0], self.grid_size[0]+self.pos[0], self.cell_size):
                for col in xrange(self.pos[1], self.grid_size[1]+self.pos[1], self.cell_size):
                    color = (random(), random(), random(), 1)
                    Color(*color)
                    Line(rectangle=(row, col, self.cell_size, self.cell_size))
                    # Rectangle(pos=(row, col), size=(self.cell_size, self.cell_size))


    def add_ball(self, b):
        self.ball = b

    def on_touch_down(self, touch):
        self.root.ball.move((touch.x, touch.y))
        # with self.canvas:
        #     Color(1, 0.2, 0,2)
        #     Rectangle(pos=(touch.x, touch.y), size=(40,40))
        


class MyPaintApp(App):

    def build(self):
        root = FloatLayout()
        root.add_widget(Field())
        root.add_widget(Ball())
        # self.add_widget(b)
        return root
        # return Field()
        # return MyPaintWidget()


if __name__ == '__main__':
    MyPaintApp().run()