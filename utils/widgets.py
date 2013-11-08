
import pygame
from pygame import Rect, Color


class WidgetError(Exception):
    pass


class LayoutError(WidgetError):
    pass


class Box(object):
    """ A rectangular box. Has a background color, and can have
        a border of a different color.
        
        Has a concept of the "internal rect". This is the rect
        inside the border (not including the border itself).
    """
    def __init__(self, 
            surface,
            rect,
            background_color,
            border_width=0,
            border_color=Color('black')):
        """ rect:
                The (outer) rectangle defining the location and
                size of the box on the surface.
            bgcolor: 
                The background color
            border_width:
                Width of the border. If 0, no border is drawn. 
                If > 0, the border is drawn inside the bounding 
                rect of the widget (so take this into account when
                computing internal space of the box).
            border_color:
                Color of the border.
        """
        self.surface = surface
        self.rect = rect
        self.bgcolor = background_color
        self.border_width = border_width
        self.border_color = border_color
        
        # Internal rectangle
        self.in_rect = Rect(
            self.rect.left + self.border_width,
            self.rect.top + self.border_width,
            self.rect.width - self.border_width * 2,
            self.rect.height - self.border_width * 2)
        
    def draw(self):
        #pygame.draw.rect(self.surface, self.border_color, self.rect)
        pygame.draw.rect(self.surface, self.bgcolor, self.in_rect)

    def get_internal_rect(self):
        """ The internal rect of the box.
        """
        #return self.rect
        return self.in_rect
