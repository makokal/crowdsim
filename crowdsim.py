import os, sys
from random import randint, choice
from math import sin, cos, radians

import pygame
from pygame import Rect, Color
from pygame.sprite import Sprite

from entities import Agent
from utils import Timer, Box, GridMap, SIM_COLORS

class Simulation(object):
    """ 
    The man simulation entry point 
    """

    SCREEN_WIDTH, SCREEN_HEIGHT = 700, 600
    GRID_SIZE = 20
    FIELD_SIZE = 700, 600
    N_AGENTS = 50


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
        self.spawn_new_agent()
        self.agent_spawn_timer = Timer(500, self.spawn_new_agent)

        # create the grid
        self.grid_nrows = self.FIELD_SIZE[1] / self.GRID_SIZE
        self.grid_ncols = self.FIELD_SIZE[0] / self.GRID_SIZE
        self.goal_coord = (self.grid_nrows - 1, self.grid_ncols - 1)

        self.options = dict(draw_grid=False)


    _spawned_agent_count = 0
    def spawn_new_agent(self):
        if self._spawned_agent_count >= 50:
            return

        self.agent_image = pygame.image.load('assets/blueagent.bmp').convert_alpha()
        
        self.agents.add(
            Agent(  agent_id = self._spawned_agent_count,
                    screen = self.screen,
                    game = self,
                    agent_image = self.agent_image,
                    field = self.field_rect,
                    init_position = ( randint(0, self.SCREEN_WIDTH), randint(0, self.SCREEN_HEIGHT)),
                    init_direction = (1, 1),
                    max_speed = 0.05))
        self._spawned_agent_count += 1


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
                
        for agent in self.agents:
            agent.draw()
        

    def run(self):
        # The main game loop
        #
        while True:
            # Limit frame speed to 30 FPS
            time_passed = self.clock.tick(30)
            
            if time_passed > 100:
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
                self.agent_spawn_timer.update(time_passed)
                
                # Update and all agents
                for agent in self.agents:
                    agent.update(time_passed)
                    # print agent.id, len(self.get_agent_neighbors(agent, 800))
                    
                self.draw()
                
            pygame.display.flip()


    def quit(self):
        sys.exit()

if __name__ == '__main__':
    sim = Simulation()
    sim.run()

        