# waypoints for agents to move to 

from utils import SIM_COLORS, SCALE
from utils import euclidean_distance
import math
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

    def normal_point(self, p1, p2, oc11, oc12, oc21, oc22):
        # TODO - clean this up, lifted directly from pedsim c++
        a1, a2 = oc11, oc12
        b1, b2 = oc21 - oc11, oc22 - oc12
        lmbda = (p1*b1 + p2*b2 - b1*a1 - b2*a2) / (b1**2 + b2**2)

        if lmbda <= 0:
            return (oc11, oc12, 0)
        elif lmbda >= 1:
            return (oc21, oc22, 0)

        return (a1 + lmbda*b1, a2 + lmbda*b2, 0)


    def attaction_force(self, agent, myx, myy, fromx, fromy):
        # TODO - clean this up
        nx, ny = ((agent.y - fromy) / euclidean_distance((agent.x, agent.y), (fromx, fromy))), \
                ((agent.x - fromx) / euclidean_distance((agent.x, agent.y), (fromx, fromy)))
        oc11, oc12 = agent.x + self.radius * nx, agent.y - self.radius * ny
        oc21, oc22 = agent.x - self.radius * nx, agent.y + self.radius * ny

        pn = self.normal_point(myx, myy, oc11, oc12, oc21, oc22)
        pdist = euclidean_distance((myx, myy), (pn[0],pn[1]))

        if pdist == 0:
            return (0, 0, 0)

        return ((pn[0]-myx)/pdist, (pn[1]-myy)/pdist, 0 )


    def force_to(self, agent):
        """ Compute the force to the waypoint (direction only)
        """
        dx, dy = self.position[0] - agent.x, self.position[1] - agent.y
        theta = math.atan2(dy, dx)
        return (math.cos(theta), math.sin(theta), 0)


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

