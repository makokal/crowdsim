from __future__ import division                 #to avoid integer devision problem


from timers import Timer
from widgets import Box
from vec2d import vec2d
from gridmap import GridMap
from colors import *
from constants import *
from custom_types import *

from math import sqrt
import random
import scipy

def euclidean_distance(a, b):
    return sqrt( (a[0]-b[0])**2 + (a[1]-b[1])**2 )


def random_position(x, y, dx, dy):
    px = random.uniform(x-dx, x+dx)
    py = random.uniform(y-dy, y+dy)
    return (px, py)

def random_fatness(alpha, beta):
    return random.betavariate(alpha, beta)



#just for fun making further development easier and with joy
pi     = scipy.pi
dot    = scipy.dot
sin    = scipy.sin
cos    = scipy.cos
ar     = scipy.array
rad    = lambda ang: ang*pi/180                 #lovely lambda: degree to radian

#the function
def Rotate2D(pts, cnt, ang=pi/4):
    '''pts = {} Rotates points(nx2) about center cnt(2) by angle ang(1) in radian'''
    return dot(pts-cnt,ar([[cos(ang),sin(ang)],[-sin(ang),cos(ang)]]))+cnt


def rotate_polygon(self, polygon, center, angle):
    """
    Polygon is represented as list of 2D points [(x,y), ...]
    """
    np =  [(vec2d(p).rotated(self._direction.get_angle())).tuple() for p in polygon]
    # return [(int(p[0]), int(p[1])) for p in np]
    return [(int(fabs(p[0])), int(fabs(p[1]))) for p in np]
    