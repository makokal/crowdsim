
from pygame.sprite import Sprite
from pygame.math import Vector2



class Agent(Sprite):
    """ A agent sprite that bounces off walls and changes its
        direction from time to time.
    """
    def __init__(self, screen, game, agent_image,
            field, init_position, init_direction, speed):
        """ Create a new Agent.
        
            screen: 
                The screen on which the agent lives (must be a 
                pygame Surface object, such as pygame.display)
            
            game:
                The game object that holds information about the
                game world.
            
            agent_image: 
                Image reprsenting the agent in the simulation
            
            field:
                A Rect specifying the 'playing field' boundaries.
                The agent will bounce off the 'walls' of this 
                field.
                
            init_position:
                A vec2d or a pair specifying the initial position
                of the agent on the screen.
            
            init_direction:
                A vec2d or a pair specifying the initial direction
                of the agent. Must have an angle that is a 
                multiple of 45 degres.
            
            speed: 
                agent speed, in pixels/millisecond (px/ms)
        """
        Sprite.__init__(self)
        
        self.screen = screen
        self.game = game
        self.speed = speed
        self.field = field
        
        # self.image is the current image representing the agent
        # in the game. It's rotated to the agent's direction.
        #
        self.image = agent_image
        
        # A vector specifying the agent's position on the screen
        #
        self.pos = Vector2(init_position)
        self.prev_pos = Vector2(self.pos)

        # The direction is a normalized vector
        #
        self.direction = Vector2(init_direction).normalize_ip()


    def draw(self):
        """ 
        Draw the agent onto the screen that is set in the constructor
        """

        self.draw_rect = self.image.get_rect().move(
            self.pos.x - self.image_w / 2, 
            self.pos.y - self.image_h / 2)
        self.screen.blit(self.image, self.draw_rect)

    def update(self, time_passed):
        pass


        