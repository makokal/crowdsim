
from pygame.sprite import Sprite
from utils import vec2d



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
        self.pos = vec2d(init_position)
        self.prev_pos = vec2d(self.pos)

        # The direction is a normalized vector
        #
        self.direction = vec2d(init_direction).normalized()


    def draw(self):
        """ 
        Draw the agent onto the screen that is set in the constructor
        """

        self.draw_rect = self.image.get_rect().move(
            self.pos.x - self.image_w / 2, 
            self.pos.y - self.image_h / 2)
        self.screen.blit(self.image, self.draw_rect)


    def update(self, time_passed):
        self._compute_direction(time_passed)
        displacement = vec2d(    
            self.direction.x * self.speed * time_passed,
            self.direction.y * self.speed * time_passed)
        
        self.prev_pos = vec2d(self.pos)
        self.pos += displacement
        
        # When the image is rotated, its size is changed.
        self.image_w, self.image_h = self.image.get_size()

    def _compute_direction(self, time_passed):
        """ Finds out where to go
        """
        coord = self.game.xy2coord(self.pos)
        
        x_mid, y_mid = self.game.coord2xy_mid(coord)
        
        if (    (x_mid - self.pos.x) * (x_mid - self.prev_pos.x) < 0 or
                (y_mid - self.pos.y) * (y_mid - self.prev_pos.y) < 0):
            next_coord = (coord[0]+1, coord[1]+1)
    
            self.direction = vec2d(
                next_coord[1] - coord[1],
                next_coord[0] - coord[0]).normalized()


        