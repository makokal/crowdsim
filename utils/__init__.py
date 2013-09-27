from timers import Timer
from widgets import Box
from vec2d import vec2d
from gridmap import GridMap
from colors import *
from constants import *

from math import sqrt

def euclidean_distance(a, b):
    return sqrt( (a[0]-b[0])**2 + (a[1]-b[1])**2 )