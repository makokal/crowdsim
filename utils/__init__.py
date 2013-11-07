from timers import Timer
from widgets import Box
from vec2d import vec2d
from gridmap import GridMap
from colors import *
from constants import *
from custom_types import *



from math import sqrt
import random

def euclidean_distance(a, b):
    return sqrt( (a[0]-b[0])**2 + (a[1]-b[1])**2 )


def random_position(x, y, dx, dy):
    px = random.uniform(x-dx, x+dx)
    py = random.uniform(y-dy, y+dy)
    return (px, py)
