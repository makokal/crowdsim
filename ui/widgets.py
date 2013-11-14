import kivy

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
    def __init__(self, **kwargs):
        super(Field, self).__init__(**kwargs)
        with self.canvas:
            Color(0.2, 0.2, 0,2)
            Rectangle(pos=(0,0), size=(600,600))


    def on_touch_down(self, touch):
        with self.canvas:
            Color(1, 0.2, 0,2)
            Rectangle(pos=(touch.x, touch.y), size=(40,40))




class GridView(Widget):
    """ The view for Grids """
    pass    