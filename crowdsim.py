import os, sys
from random import randint, choice, normalvariate
from math import sin, cos, radians

import pygame
from pygame import Rect
from pygame.locals import *

from entities import Agent, Waypoint, Obstacle
from utils import Timer, Box, GridMap, SIM_COLORS, random_position
from controllers import SocialForceController, RandomController

class Simulation(object):
    """ 
    The main simulation entry point 
    """

    # basic defaults
    SCREEN_WIDTH, SCREEN_HEIGHT = 700, 600
    GRID_SIZE = 20
    FIELD_SIZE = 700, 600
    FIELD_BORDER_WIDTH = 5

    def __init__(self, params=None):
        pygame.init()

        if params is not None:
            self.SCREEN_HEIGHT = int(params['display']['height'])
            self.SCREEN_WIDTH = int(params['display']['width'])
            self.GRID_SIZE = int(params['cell']['width'])
            self.FIELD_SIZE = self.SCREEN_HEIGHT, self.SCREEN_WIDTH


        # setup the screen and the box field of play 
        self.initialize_screen()

        # agents
        self.agents = pygame.sprite.Group()
        self.agent_image = pygame.image.load('assets/blueagent.bmp').convert_alpha()
        self.controller = SocialForceController(self)
        # self.controller = RandomController(self)


        # time related items
        self.clock = pygame.time.Clock()
        self.paused = False
        self.simulation_timer = Timer(50, self.simulation_update)

        # create the grid
        self.setup_grid()

        # additional options (remove this)
        self.options = dict(draw_grid=True)

        # setup objects (waypoints, obstacles)
        self.waypoints = dict()
        self.obstacles = []
        self._agent_count = 0


    def initialize_screen(self):
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), HWSURFACE|DOUBLEBUF|RESIZABLE, 32)
        self.field_border_width = self.FIELD_BORDER_WIDTH
        self.field_rect_outer = Rect(0, 0, self.FIELD_SIZE[0], self.FIELD_SIZE[1])
        self.field_bgcolor = SIM_COLORS['black']
        self.field_border_color = SIM_COLORS['red']
        self.field_box = Box(self.screen, 
            rect=self.field_rect_outer, 
            bgcolor=self.field_bgcolor,
            border_width=self.field_border_width,
            border_color=self.field_border_color)

        self.field_rect = self.get_field_rect()


    def setup_grid(self):
        self.grid_nrows = self.FIELD_SIZE[1] / self.GRID_SIZE
        self.grid_ncols = self.FIELD_SIZE[0] / self.GRID_SIZE
        self.goal_coord = (self.grid_nrows - 1, self.grid_ncols - 1)


    def get_field_rect(self):
        """ Return the internal field rect - the rect of the game
            field exluding its border.
        """
        return self.field_box.get_internal_rect()


    def get_agent_neighbors(self, agent, dist_range):
        neighbors =  []
        for other in self.agents:
            if not agent.id == other.id:
                dist = agent.position.get_distance(other.position)
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
       
        # agents
        self.agents.add(
                Agent(  agent_id = 0,
                    screen = self.screen,
                    game = self,
                    agent_image = self.agent_image,
                    field = self.field_rect,
                    init_position = ( 3, 1),
                    init_direction = (1, 1),
                    max_speed = 1.8,
                    waypoints = [self.waypoints['stop'], self.waypoints['start']]
                    )
            )
        self.agents.add(
                Agent(  agent_id = 1,
                    screen = self.screen,
                    game = self,
                    agent_image = self.agent_image,
                    field = self.field_rect,
                    init_position = ( 3, 5),
                    init_direction = (1, 1),
                    max_speed = 1.8,
                    waypoints = [self.waypoints['start'], self.waypoints['stop']]
                    )
            )

        self.agents.add(
                Agent(  agent_id = 2,
                    screen = self.screen,
                    game = self,
                    agent_image = self.agent_image,
                    field = self.field_rect,
                    init_position = ( 2, 2),
                    init_direction = (1, 1),
                    max_speed = 1.14,
                    waypoints = [self.waypoints['start'], self.waypoints['stop']]
                    )
            )


    def simulation_update(self):
        for agent in self.agents:
            agent.update(0.1)
            self.controller.drive_single_step(agent, delta_time=0.1)
            agent.draw()
        self.draw()



    def _process_events(self):
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
            elif event.type == VIDEORESIZE:
                self.SCREEN_WIDTH, self.SCREEN_HEIGHT = event.dict['size']
                self.FIELD_SIZE = self.SCREEN_WIDTH, self.SCREEN_HEIGHT     # TODO - decouple this (field need be constant)
                self.initialize_screen()
                self.setup_grid()


    _total_time = 0

    def run(self):
        # initialize modules
        pygame.init()

        # populate the scene
        # self.demo_populate_scene()

        while True:
            self.time_passed = self.clock.tick()

            # self._total_time += self.time_passed
            # if self._total_time < 1000:
            #     continue
            
            # handle any events
            self._process_events()
            
            if not self.paused:     
                self.simulation_timer.update(self.time_passed)
            
            # update the game surface
            pygame.display.flip()





    def add_agents(self, agent_dict):
        for agent in agent_dict:
            dx, dy = float(agent['dx']), float(agent['dy'])
            x, y = float(agent['x']), float(agent['y'])
            num = int(agent['n'])
            a_type = int(agent['type'])

            # spawn an agent in a random direction and position(within dx, dy)
            direction = (randint(-1, 1), randint(-1, 1))
            position = random_position(x, y, dx, dy)
            waypoints = [awp['id'] for awp in agent['addwaypoint']]

            for _ in xrange(num):
                self.agents.add(Agent(
                        agent_id = self._agent_count,
                        atype = a_type,
                        screen = self.screen,
                        game = self,
                        agent_image = self.agent_image,
                        field = self.field_rect,
                        init_position = position,
                        init_direction = direction,
                        max_speed = normalvariate(1.34, 0.26),
                        waypoints = [self.waypoints[wp] for wp in waypoints]
                    ))
                self._agent_count += 1

        # we are done here
        # TODO - move the velocity stuff to a neat function


    
    def add_waypoints(self, waypoint_dict):
        for waypoint in waypoint_dict:
            w_id = waypoint['id']
            radius = float(waypoint['radius'])
            wtype = waypoint['type']
            x, y = float(waypoint['x']), float(waypoint['y'])
            self.waypoints.update({w_id : Waypoint(screen=self.screen, wid=w_id, wtype=wtype, position=(x, y), radius=radius)})


    def add_obstacles(self, obstacle_dict):
        for obstacle in obstacle_dict:
            o_id = obstacle['id']
            p1 = float(obstacle['p1'])
            p2 = float(obstacle['p2'])
            p3 = float(obstacle['p3'])
            p4 = float(obstacle['p4'])
            o_type = obstacle['type'].title()
            self.obstacles.append(Obstacle(screen=self.screen, oid=o_id, otype=o_type, params=(p1, p2, p3, p4)))


    
    def quit(self):
        sys.exit()

        