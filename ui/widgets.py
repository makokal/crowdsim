import kivy

from random import random

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Line, Rectangle

class AgentView(Widget):
    """ The view for agents """
    pass 


class WaypointView(Widget):
    """ The view for Waypoints """
    pass 


class ObstacleView(Widget):
    """ The view for Obstacles """
    pass    


class Cell(Widget):
    def __init__(self, px, py):
        super(Cell, self).__init__()
        self.px, self.py = px, py
        with self.canvas:
            Color(1, 0.2, 0,2)
            Rectangle(pos=(self.px, self.py), size=(40,40))


class Field(Widget):
    cell_size = 40
    grid_size = 400, 400
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
            for row in xrange(self.pos[0], self.grid_size[0], self.cell_size):
                for col in xrange(self.pos[1], self.grid_size[1], self.cell_size):
                    color = (random(), random(), random(), 1)
                    Color(*color)
                    Rectangle(pos=(row, col), size=(self.cell_size, self.cell_size))


    # def on_touch_down(self, touch):
    #     with self.canvas:
    #         Color(1, 0.2, 0,2)
    #         Rectangle(pos=(touch.x, touch.y), size=(40,40))




class GridView(Widget):
    """ The view for Grids """
    pass    