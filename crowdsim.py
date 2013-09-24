import pygame
import sys

from entities import Agent
from utils import Timer

class Simulation(object):
    """ 
    The man simulation entry point 
    """

    SCREEN_WIDTH, SCREEN_HEIGHT = 400, 400
    BG_COLOR = 0,0,0
    CREEP_FILENAMES = [
        'bluecreep.png', 
        'pinkcreep.png', 
        'graycreep.png']
    N_agents = 20


    def __init__(self, args=None):
        pygame.init()
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), 0, 32)
        # self.field_rect = self.get_field_rect()


    def run(self):
        clock = pygame.time.Clock()

        # create agents 
        self.agents = pygame.sprite.Group()
        img = pygame.image.load("assets/blueagent.png",'blueagnet.png').convert_alpha()

        self.agents.add(
            Agent(  screen = self.screen,
                    game = self,
                    agent_image = img,
                    field = (40, 10, 40, 20),
                    init_position = ( 20, 20),
                    init_direction = (1, 1),
                    speed=0.05))

        while True:
            # Limit frame speed to 50 FPS
            #
            time_passed = clock.tick(50)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            
            # Redraw the background
            self.screen.fill(self.BG_COLOR)
            
            # Update and redraw all creeps
            for agent in self.agents:
                agent.update(time_passed)
                agent.draw()

            pygame.display.flip()


if __name__ == '__main__':
    sim = Simulation()
    sim.run()

        