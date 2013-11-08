import os, sys
from random import randint, choice, normalvariate
from math import sin, cos, radians

import pygame
from pygame import Rect
from pygame.locals import *

from entities import Agent, Waypoint, Obstacle
from utils import Timer, Box, GridMap, SIM_COLORS, SCALE, random_position, random_fatness
from controllers import SocialForceController, RandomController


class Simulation(object):
    """ 
    The main simulation entry point 
    """

    # basic defaults
    SCREEN_WIDTH, SCREEN_HEIGHT = 700, 700
    GRID_SIZE = 20, 20
    FIELD_SIZE = 500, 500
    FIELD_LIMITS = 0, 0, 600, 600
    field_bgcolor = SIM_COLORS['white']

    def __init__(self, params=None):
        pygame.init()

        if params is not None:
            self.SCREEN_HEIGHT, self.SCREEN_WIDTH = int(float(params['display']['height']) * SCALE), \
                                                    int(float(params['display']['width']) * SCALE)
            self.FIELD_LIMITS = int(float(params['field_top_left_x']) * SCALE), \
                                int(float(params['field_top_left_y']) * SCALE), \
                                int(float(params['field_bottom_right_x']) * SCALE), \
                                int(float(params['field_bottom_right_y']) * SCALE)
            self.FIELD_SIZE = self.FIELD_LIMITS[2] - self.FIELD_LIMITS[0], self.FIELD_LIMITS[3] - self.FIELD_LIMITS[1]
            self.GRID_SIZE = int(float(params['cell']['width']) * SCALE), int(float(params['cell']['height']) * SCALE)

        # zoom and centering
        self.offset = 0, 0
        self.zoom_factor = 1.0
        self._old_screen = self.SCREEN_WIDTH, self.SCREEN_HEIGHT

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
        self.simulation_timer = Timer(10, self.simulation_update)

        # create the grid
        self.setup_grid()

        # additional options (remove this)
        self.options = dict(draw_grid=True)

        # setup objects (waypoints, obstacles)
        self.waypoints = dict()
        self.obstacles = []
        self._agent_count = 0

        # initialize the time
        self.time_passed = 0


    def initialize_screen(self):
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT),
                                              HWSURFACE | DOUBLEBUF | RESIZABLE, 32)
        self.field_rect_outer = Rect(self.FIELD_LIMITS[0],
                                     self.FIELD_LIMITS[1],
                                     int(self.FIELD_SIZE[0]*self.zoom_factor),
                                     int(self.FIELD_SIZE[1]*self.zoom_factor))

        self.field_box = Box(surface=self.screen,
            rect=self.field_rect_outer, 
            background_color=self.field_bgcolor
        )

        self.field_rect = self.field_box.get_internal_rect()

    def setup_grid(self):
        self.grid_nrows = self.FIELD_SIZE[1] / int(self.GRID_SIZE[0]*self.zoom_factor)
        self.grid_ncols = self.FIELD_SIZE[0] / int(self.GRID_SIZE[1]*self.zoom_factor)

    def get_agent_neighbors(self, agent, dist_range):
        neighbors = []
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
                (self.field_rect.left, self.field_rect.top + y * int(self.GRID_SIZE[1]*self.zoom_factor) - 1),
                (self.field_rect.right - 1, self.field_rect.top + y * int(self.GRID_SIZE[1]*self.zoom_factor) - 1))
        
        for x in range(self.grid_ncols + 1):
            pygame.draw.line(
                self.screen,
                SIM_COLORS['light gray'],
                (self.field_rect.left + x * int(self.GRID_SIZE[0]*self.zoom_factor) - 1, self.field_rect.top),
                (self.field_rect.left + x * int(self.GRID_SIZE[0]*self.zoom_factor) - 1, self.field_rect.bottom - 1))

    def xy2coord(self, pos):
        """ Convert a (x, y) pair to a (nrow, ncol) coordinate
        """
        x, y = (pos[0] - self.field_rect.left, pos[1] - self.field_rect.top)
        return int(y) / self.GRID_SIZE[1], int(x) / self.GRID_SIZE[0]
    
    def coord2xy_mid(self, coord):
        """ Convert a (nrow, ncol) coordinate to a (x, y) pair,
            where x,y is the middle of the square at the coord
        """
        nrow, ncol = coord
        return (
            self.field_rect.left + ncol * self.GRID_SIZE[0] + self.GRID_SIZE[0] / 2,
            self.field_rect.top + nrow * self.GRID_SIZE[1] + self.GRID_SIZE[1] / 2)

    def draw_background(self):
        pygame.draw.rect(self.screen, SIM_COLORS['light gray'], [0, 0, self.SCREEN_WIDTH, self.SCREEN_HEIGHT])

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
                elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                    #self.zoom_factor += 0.1
                    self.initialize_screen()
                    self.setup_grid()
                elif event.key == pygame.K_MINUS:
                    #self.zoom_factor -= 0.1
                    self.initialize_screen()
                    self.setup_grid()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pass
            elif event.type == VIDEORESIZE:
                self._old_screen = self.SCREEN_WIDTH, self.SCREEN_HEIGHT
                self.SCREEN_WIDTH, self.SCREEN_HEIGHT = event.dict['size']

                self.offset = self.SCREEN_WIDTH - self._old_screen[0], self.SCREEN_HEIGHT - self._old_screen[1]
                #self.FIELD_LIMITS = self.FIELD_LIMITS[0]+self.offset[0], self.FIELD_LIMITS[1]+self.offset[1], \
                #                    self.FIELD_LIMITS[2], self.FIELD_LIMITS[3]

                #fx = (self.SCREEN_WIDTH / 2) - (self.FIELD_SIZE[0] / 2)
                #fy = (self.SCREEN_HEIGHT / 2) - (self.FIELD_SIZE[1] / 2)
                #self.FIELD_LIMITS = fx, fy, self.FIELD_LIMITS[2], self.FIELD_LIMITS[3]

                self.initialize_screen()
                self.setup_grid()

    _total_time = 0

    def run(self):
        # initialize modules
        pygame.init()

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

            rd = 0.3

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
                        radius = rd,
                        waypoints = [self.waypoints[wp] for wp in waypoints]
                    ))
                self._agent_count += 1

        # we are done here
        # TODO - move the velocity stuff to a neat function
        # TODO - find a suitable fatness distribution
    
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
