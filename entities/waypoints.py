# waypoints for agents to move to 

from utils import SIM_COLORS, SCALE
import pygame

class Waypoint(object):
    """ Agent waypoints in the scene """
    def __init__(self, screen, wid, wtype, position, radius):
        """
            screen:
                The screen on which the waypoint lives
            wid:
                waypoint id
            wtype: 
                waypoint type (birth, death, normal)
            position:
                2D location of the waypoint in (x,y) format in metres
            radius:
                Radius of the waypoint (all waypoints are circular) in metres
        """
        self.screen = screen
        self._id = wid
        self._type = wtype
        self._position = (position[0]*SCALE, position[1]*SCALE)  # stored internally in pixels
        self._radius = radius * SCALE # stored internally in pixels


    def draw(self):
        """  draw waypoints as filled circles. All drawing works in px units
        """
        pygame.draw.circle(
            self.screen, 
            SIM_COLORS['maroon'], 
            (int(self._position[0]), int(self._position[1])), 
            int(self._radius), 
            int(0))



    @property
    def id(self):
        return self._id

    @property
    def type(self):
        return self._type

    @property
    def position(self):
        return (self._position[0] / SCALE, self._position[1] / SCALE)

    @property
    def radius(self):
        return self._radius / SCALE


