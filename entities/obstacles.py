# obstacles for the scene

import pygame
from utils import SIM_COLORS, SCALE

class Obstacle(object):
    """ Scene obstacles """
    def __init__(self, screen, oid, otype, params):
        """
            screen:
                Obstacles exists on a screen element 
            oid:
                obstacle id 
            otype: 
                obstacle type (Line, Rect, Circle)
            params:
                Obstacle parameters according to the type. This in the form 
                of: Circle -> [x,y,r,None], Line -> [x1,y1,x2,y2] and 
                Rect -> [x,y,w,h]
        """
        self.screen = screen
        self._id = oid
        self._type = otype
        self._params = (params[0]*SCALE, params[1]*SCALE, params[2]*SCALE, params[3]*SCALE)


    def draw(self):
        """  draw obstacle with respective shape
        """
        if self.type == 'Circle':
            pygame.draw.circle(
                self.screen, 
                SIM_COLORS['blue'], 
                (int(self._params[0]), int(self._params[1])), 
                int(self._params[2]), 
                0)
        elif self.type == 'Line':
            pygame.draw.line(
                self.screen,
                SIM_COLORS['blue'],
                (int(self._params[0]), int(self._params[1])),
                (int(self._params[2]), int(self._params[3])))
        elif self.type == 'Rect':
            pygame.draw.rect(
                self.screen,
                SIM_COLORS['blue'],
                (int(self._params[0]), int(self._params[1]),
                int(self._params[2]), int(self._params[3])) )


    def convert_to_cells(self, grid):
        pass


    @property
    def id(self):
        return self._id

    @property
    def type(self):
        return self._type

    @property
    def params(self):
        return (self._params[0] / SCALE, self._params[1] / SCALE, self._params[2] / SCALE, self._params[3] / SCALE)
