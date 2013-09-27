import os, sys
from random import randint, choice
from math import sin, cos, radians

import pygame
from pygame import Rect, Color
from pygame.sprite import Sprite

from entities import Agent, Waypoint, Obstacle
from utils import Timer, Box, GridMap, SIM_COLORS, SCALE

class Simulation(object):
    """ 
    The main simulation entry point 
    """

    SCREEN_WIDTH, SCREEN_HEIGHT = 700, 600
    GRID_SIZE = 20
    FIELD_SIZE = 700, 600

    def __init__(self, args=None):
        pygame.init()
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), 0, 32)
        self.field_border_width = 4
        self.field_rect_outer = Rect(0, 0, self.FIELD_SIZE[0], self.FIELD_SIZE[1])
        self.field_bgcolor = SIM_COLORS['black']
        self.field_border_color = SIM_COLORS['red']
        self.field_box = Box(self.screen, 
            rect=self.field_rect_outer, 
            bgcolor=self.field_bgcolor,
            border_width=self.field_border_width,
            border_color=self.field_border_color)

        self.field_rect = self.get_field_rect()

        self.clock = pygame.time.Clock()
        self.paused = False

        # agents
        self.agents = pygame.sprite.Group()

        self.simulation_timer = Timer(50, self.simulation_update)

        # create the grid
        self.grid_nrows = self.FIELD_SIZE[1] / self.GRID_SIZE
        self.grid_ncols = self.FIELD_SIZE[0] / self.GRID_SIZE
        self.goal_coord = (self.grid_nrows - 1, self.grid_ncols - 1)

        self.options = dict(draw_grid=False)

        self.agent_image = pygame.image.load('assets/blueagent.bmp').convert_alpha()



    def get_field_rect(self):
        """ Return the internal field rect - the rect of the game
            field exluding its border.
        """
        return self.field_box.get_internal_rect()


    def get_agent_neighbors(self, agent, dist_range):
        neighbors =  []
        for other in self.agents:
            if not agent.id == other.id:
                dist = agent.pos.get_distance(other.pos)
                if dist <= dist_range:
                    neighbors.append(other)

        return neighbors


    def draw_grid(self):
        for y in range(self.grid_nrows + 1):
            pygame.draw.line(
                self.screen,
                SIM_COLORS['light gray'],
                (self.field_rect.left, self.field_rect.top + y * self.GRID_SIZE - 1),
                (self.field_rect.right - 1, self.field_rect.top + y * self.GRID_SIZE - 1))
        
        for x in range(self.grid_ncols + 1):
            pygame.draw.line(
                self.screen,
                SIM_COLORS['light gray'],
                (self.field_rect.left + x * self.GRID_SIZE - 1, self.field_rect.top),
                (self.field_rect.left + x * self.GRID_SIZE - 1, self.field_rect.bottom - 1))
        
    
    def xy2coord(self, pos):
        """ Convert a (x, y) pair to a (nrow, ncol) coordinate
        """
        x, y = (pos[0] - self.field_rect.left, pos[1] - self.field_rect.top)
        return (int(y) / self.GRID_SIZE, int(x) / self.GRID_SIZE)
    
    def coord2xy_mid(self, coord):
        """ Convert a (nrow, ncol) coordinate to a (x, y) pair,
            where x,y is the middle of the square at the coord
        """
        nrow, ncol = coord
        return (
            self.field_rect.left + ncol * self.GRID_SIZE + self.GRID_SIZE / 2, 
            self.field_rect.top + nrow * self.GRID_SIZE + self.GRID_SIZE / 2)


    def draw_background(self):
        bk_color = SIM_COLORS['gray']
        x, y = 0, 0
        width, height = self.SCREEN_WIDTH, self.SCREEN_HEIGHT

        pygame.draw.rect(self.screen, bk_color, 
            [x, y, width, height])


    def draw(self):
        self.draw_background()
        self.field_box.draw()
        
        if self.options['draw_grid']:
            self.draw_grid()
                
        for waypoint in self.waypoints:
            self.waypoints[waypoint].draw()

        for obstacle in self.obstacles:
            obstacle.draw()

        for agent in self.agents:
            agent.draw()


    def demo_populate_scene(self):
        # popupate the scene with waypoints, obstacles and agents
        # waypoints
        self.waypoints = {
        'start': Waypoint(self.screen, 'start', 'normal', (2,1), 0.3),
        'stop': Waypoint(self.screen, 'stop', 'normal', (4,5), 0.3),
        'fuel': Waypoint(self.screen, 'fuel', 'normal', (6,2), 0.3)
        }

        # agents
        self.agents.add(
                Agent(  agent_id = 0,
                    screen = self.screen,
                    game = self,
                    agent_image = self.agent_image,
                    field = self.field_rect,
                    init_position = ( 1, 1),
                    init_direction = (1, 1),
                    max_speed = 0.5,
                    waypoints = [self.waypoints['stop'], self.waypoints['start'], self.waypoints['fuel']]
                    )
            )
        self.agents.add(
                Agent(  agent_id = 1,
                    screen = self.screen,
                    game = self,
                    agent_image = self.agent_image,
                    field = self.field_rect,
                    init_position = ( 5, 4),
                    init_direction = (1, 1),
                    max_speed = 0.25,
                    waypoints = [self.waypoints['start'], self.waypoints['stop'], self.waypoints['fuel']]
                    )
            )

        # add some obstacles
        self.obstacles = []
        self.obstacles.append(Obstacle(self.screen, 'box', 'Rect', (2,3,1,1)))
        # self.obstacles.append(Obstacle(self.screen, 'line', 'Line', (4,3,3,4)))
        self.obstacles.append(Obstacle(self.screen, 'tree', 'Circle', (4,1,0.5,0)))



    def simulation_update(self):
        for agent in self.agents:
            agent.update(1)
            agent.draw()
        self.draw()


    def run(self):
        # The main game loop
        
        # populate the scene
        self.demo_populate_scene()

        while True:
            # Limit frame speed to 30 FPS
            self.time_passed = self.clock.tick(30)
            
            if self.time_passed > 100:
                continue
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.paused = not self.paused
                    elif event.key == pygame.K_g:
                        if pygame.key.get_mods() & pygame.KMOD_CTRL:
                            self.options['draw_grid'] = not self.options['draw_grid']
                elif (  event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
                    pass
            
            if not self.paused:     
                self.simulation_timer.update(self.time_passed)
                
                # Update and all agents
                # for agent in self.agents:
                    # agent.update(time_passed)
                    
                # self.draw()
                
            pygame.display.flip()


    def quit(self):
        sys.exit()

if __name__ == '__main__':
    sim = Simulation()
    sim.run()

        