# obstacles for the scene

import pygame
from utils import SIM_COLORS, SCALE
from utils import euclidean_distance, vec2d

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
            pygame.draw.circle(self.screen, SIM_COLORS['blue'], 
                (int(self._params[0]), int(self._params[1])), 
                int(self._params[2]), 
                0)
        elif self.type == 'Line':
            pygame.draw.line(self.screen, SIM_COLORS['blue'],
                (int(self._params[0]), int(self._params[1])),
                (int(self._params[2]), int(self._params[3])), 5)
        elif self.type == 'Rect':
            pygame.draw.rect(self.screen, SIM_COLORS['blue'],
                (int(self._params[0]), int(self._params[1]),
                int(self._params[2]), int(self._params[3])) )



    def agent_distance(self, agent):
        """ Compute the distance from obstacle boundary to agent 
            Return a pair dist, point where point is the closet 
            point on the obstacle to the agent
        """
        if self.type == 'Line':
            return self._line_intersection(self.params, (agent._position.x, agent._position.y))
        elif self.type == 'Circle':
            return self._circle_intersection(self.params, (agent._position.x, agent._position.y))
        elif self.type == 'Rect':
            x, y, w, h = self.params
            candidates = dict()
            d1, p1 = self._line_intersection((x, y, x+w, y), (agent._position.x, agent._position.y))
            d2, p2 = self._line_intersection((x, y, x, y+h), (agent._position.x, agent._position.y))
            d3, p3 = self._line_intersection((x+w, y, x+w, y+h), (agent._position.x, agent._position.y))
            d4, p4 = self._line_intersection((x, y+h, x+w, y+h), (agent._position.x, agent._position.y))
            candidates[d1] = p1
            candidates[d2] = p2
            candidates[d3] = p3
            candidates[d4] = p4

            keylist = candidates.keys()
            keylist.sort()

            return keylist[0], candidates[keylist[0]]


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


    def _line_intersection(self, line, point):
        """ Fine the point of intersetion of a line and a point 
            Line is given as (x1,y1, x2,y2), point (x,y)

            based on http://paulbourke.net/geometry/pointlineplane/
        """
        den = euclidean_distance((line[0],line[1]), (line[2],line[3]))
        x1, y1, x2, y2 = line[0], line[1], line[2], line[3]
        x3, y3 = point[0], point[1]

        u = ( ((x3-x1) * (x2-x1)) + ((y3-y1) * (y2-y1)) ) / den

        x, y = (x1 + u * (x2-x1)), (y1 + u * (y2-y1))
        dist = euclidean_distance((x,y), point)

        # pygame.draw.circle(self.screen, SIM_COLORS['aqua'], 
        #         (int(x*SCALE), int(y*SCALE)), 
        #         int(40), 
        #         0)
        # print dist*SCALE, (x*SCALE,y*SCALE)

        return dist, (x, y)


    def _circle_intersection(self, circle, point):
        """ Compute the distance and point on the boundary of the circle
            intersected by a line from its center to the point
        """
        dist = euclidean_distance((circle[0], circle[1]), point) - circle[2]
        vun = vec2d((circle[0] - point[0]), (circle[1] - point[1]))
        v = vun.normalized()

        x, y = (point[0] + dist * v.x), (point[0] + dist * v.x)

        return dist, (x, y)

