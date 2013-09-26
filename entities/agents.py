
from random import randint, choice
from math import sin, cos, radians, exp, sqrt

import pygame
from pygame.sprite import Sprite
from pygame.math import Vector3
from utils import vec2d, SIM_COLORS



class Agent(Sprite):
    """ A agent sprite that bounces off walls and changes its
        direction from time to time.
    """

    def __init__(self, agent_id, screen, game, agent_image,
            field, init_position, init_direction, max_speed):
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
            
            max_speed: 
                maximum agent speed, in pixels/millisecond (px/ms)
        """
        Sprite.__init__(self)
        
        self.id  = agent_id
        self.screen = screen
        self.game = game
        self.max_speed = max_speed
        self.field = field
        
        # self.image is the current image representing the agent
        self.image = agent_image
        
        # A vector specifying the agent's position on the screen
        self.pos = vec2d(init_position)
        self.prev_pos = vec2d(self.pos)

        # The direction is a normalized vector
        self.direction = vec2d(init_direction).normalized()


    def draw(self):
        """ 
        Draw the agent onto the screen that is set in the constructor
        """

        self.draw_rect = self.image.get_rect().move(
            self.pos.x - self.image_w / 2, 
            self.pos.y - self.image_h / 2)
        self.screen.blit(self.image, self.draw_rect)

        # draw the direction of the agent
        pygame.draw.line(
                self.screen,
                SIM_COLORS['red'],
                (self.pos.x, self.pos.y),
                (self.pos.x + self.direction.x*20, self.pos.y + self.direction.y*20))

        # agent horizon
        pygame.draw.circle(self.screen, SIM_COLORS['yellow'], (int(self.pos.x), int(self.pos.y)), 100, int(1))


    def update(self, time_passed):        
        # self._change_direction(time_passed)

        # displacement = vec2d(    
        #     self.direction.x * self.max_speed * time_passed,
        #     self.direction.y * self.max_speed * time_passed)
            
        # self.prev_pos = vec2d(self.pos)
        # self.pos += displacement


        self.social_move(time_passed)

        
        # When the image is rotated, its size is changed.
        self.image_w, self.image_h = self.image.get_size()
        bounds_rect = self.screen.get_rect().inflate(-self.image_w, -self.image_h)
        
        if self.pos.x < bounds_rect.left:
            self.pos.x = bounds_rect.left
            self.direction.x *= -1
        elif self.pos.x > bounds_rect.right:
            self.pos.x = bounds_rect.right
            self.direction.x *= -1
        elif self.pos.y < bounds_rect.top:
            self.pos.y = bounds_rect.top
            self.direction.y *= -1
        elif self.pos.y > bounds_rect.bottom:
            self.pos.y = bounds_rect.bottom
            self.direction.y *= -1


    def social_move(self, time_passed):
        # force is computed over neighbors with 0.5m radius (= 0.5*100 px)
        _social_neighbors = self.game.get_agent_neighbors(self, (0.5*100))

        # compute the forces
        self._social_force = self._compute_social_force()
        self._compute_desired_force()
        self._compute_obstacle_force()
        self._compute_lookahead_force()

        # sum up all the forces
        forces = Vector3(0, 0, 0)
        forces[0] = self.social_force[0] + self.obstacle_force[0] + self.desired_force[0] + self.lookahead_force[0]
        forces[1] = self.social_force[1] + self.obstacle_force[1] + self.desired_force[1] + self.lookahead_force[1]
        forces[2] = self.social_force[2] + self.obstacle_force[2] + self.desired_force[2] + self.lookahead_force[2]

        # calculate the velocity based on the acceleration (forces) and momentum
        velocity = Vector3(0, 0, 0)
        momentum = 0.75

        velocity[0] = momentum * self.vx + forces[0]
        velocity[1] = momentum * self.vy + forces[1]
        velocity[2] = 0.0 # TODO - add z dimension

        # check is resulting speed is beyond maximum speed
        if velocity.length() > self.max_speed:
            velocity[0] = (velocity[0] / velocity.length()) * self.max_speed
            velocity[1] = (velocity[1] / velocity.length()) * self.max_speed
            velocity[2] = (velocity[2] / velocity.length()) * self.max_speed

        # update positions
        displacement = vec2d(velocity[0] * time_passed, velocity[1] * time_passed)
        self.prev_pos = vec2d(self.pos)
        self.pos += displacement


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

    _counter = 0
    
    def _change_direction(self, time_passed):
        """ Turn by 45 degrees in a random direction once per
            0.2 to 0.3 seconds.
        """
        self._counter += time_passed
        if self._counter > randint(200, 300):
            self.direction.rotate(45 * randint(-1, 1))
            self._counter = 0


    """ =================================================================  
        Properties and how to compute them
        =================================================================  
    """
    _social_force = Vector3(0, 0, 0)
    _desired_force = Vector3(0, 0, 0)
    _obstacle_force = Vector3(0, 0, 0)
    _lookahead_force = Vector3(0, 0, 0)
    _vx = 0.0
    _vy = 0.0 
    _ax = 0.0 
    _ay = 0.0 
    _social_neighbors = []


    @property
    def social_force(self):
        return self._social_force

    @property
    def obstacle_force(self):
        return self._obstacle_force

    @property
    def desired_force(self):
        return self._desired_force

    @property
    def lookahead_force(self):
        return self._lookahead_force

    @property
    def x(self):
        return self.pos.x

    @property
    def y(self):
        return self.pos.y

    @property
    def vx(self):
        return self._vx

    @property
    def vy(self):
        return self._vy

     

    def _compute_social_force(self):
        social_force = Vector3(0, 0, 0)

        for neighbor in self._social_neighbors:
            force = Vector3(0, 0, 0)

            if not neighbor.id == self.id:
                dist = self.pos.get_distance(neighbor.pos)
                exp_dist = exp(sqrt(dist) - 1)

                # [2cm - 20m] range
                if dist > (0.02 * 100) and dist < (20*100):
                    force[0] = (neighbor.pos.x - self.pos.x) / exp_dist
                    force[1] = (neighbor.pos.y - self.pos.y) / exp_dist

                social_force[0] = force[0]
                social_force[1] = force[1]
                social_force[2] = force[2]

        return social_force



    def _compute_desired_force(self):
        self._desired_force = Vector3(0, 0, 0)

    def _compute_obstacle_force(self):
        self._obstacle_force = Vector3(0, 0, 0)

    def _compute_lookahead_force(self):
        self._lookahead_force = Vector3(0, 0, 0)