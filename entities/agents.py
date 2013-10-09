
from random import randint, choice
from math import sin, cos, radians, exp, sqrt

import pygame
from pygame.sprite import Sprite
from pygame.math import Vector3
from utils import SIM_COLORS, SCALE
from utils import euclidean_distance, vec2d


class Agent(Sprite):
    """ A agent sprite that bounces off walls and changes its
        direction from time to time.
    """

    def __init__(self, agent_id, screen, game, agent_image,
            field, init_position, init_direction, max_speed, waypoints):
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
                of the agent on the screen in metres
            
            init_direction:
                A vec2d or a pair specifying the initial direction
                of the agent. Must have an angle that is a 
                multiple of 45 degres.
            
            max_speed: 
                maximum agent speed, in (m/s)

            waypoints:
                a list of waypoints for the agent to follow
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
        self._vx, self._vy = self.direction[0], self.direction[1]

        self._waypoints = waypoints
        self._waypoint_index = 0


    def draw(self):
        """ 
        Draw the agent onto the screen that is set in the constructor
        """

        self.draw_rect = self.image.get_rect().move(
            (self.pos.x*SCALE) - self.image_w / 2, 
            (self.pos.y*SCALE) - self.image_h / 2)
        self.screen.blit(self.image, self.draw_rect)

        # draw the forces on the agent
        self.draw_forces()

        # agent horizon
        pygame.draw.circle(self.screen, SIM_COLORS['yellow'], (int(self.pos.x*SCALE), int(self.pos.y*SCALE)), 50, int(1))


    def draw_forces(self):
        # desired force
        pygame.draw.line(self.screen, SIM_COLORS['red'],
                ((self.pos.x*SCALE), (self.pos.y*SCALE)),
                ((self.pos.x*SCALE) + self.desired_force[0]*SCALE, (self.pos.y*SCALE) + self.desired_force[1]*SCALE))

        # social force
        pygame.draw.line(self.screen, SIM_COLORS['green'],
                ((self.pos.x*SCALE), (self.pos.y*SCALE)),
                ((self.pos.x*SCALE) + self.social_force[0]*SCALE, (self.pos.y*SCALE) + self.social_force[1]*SCALE))

        # obstacle force
        pygame.draw.line(self.screen, SIM_COLORS['aqua'],
                ((self.pos.x*SCALE), (self.pos.y*SCALE)),
                ((self.pos.x*SCALE) + self.obstacle_force[0]*SCALE, (self.pos.y*SCALE) + self.obstacle_force[1]*SCALE))



    def reached_waypoint(self, waypoint):
        """ Check if the agent has reached the given waypoint so we 
            advance to the next one. Reaching means being in the 
            waypoint circle
        """
        if euclidean_distance((self.x, self.y), waypoint.position) <= waypoint.radius:
            return True
        else:
            return False


    def update(self, time_passed):        
        # self._change_direction(time_passed / 1000.0)
        # displacement = vec2d(    
        #     self.direction.x * self.max_speed * (time_passed / 1000.0),
        #     self.direction.y * self.max_speed * (time_passed / 1000.0))            
        # self.prev_pos = vec2d(self.pos)
        # self.pos += displacement

        self.social_move(time_passed / 1000.0)
        
        # When the image is rotated, its size is changed.
        self.image_w, self.image_h = self.image.get_size()
        bounds_rect = self.screen.get_rect().inflate(-self.image_w, -self.image_h)
        
        if self.pos.x*SCALE < bounds_rect.left:
            self.pos.x = bounds_rect.left/SCALE
            self.direction.x *= -1
        elif self.pos.x*SCALE > bounds_rect.right:
            self.pos.x = bounds_rect.right/SCALE
            self.direction.x *= -1
        elif self.pos.y*SCALE < bounds_rect.top:
            self.pos.y = bounds_rect.top/SCALE
            self.direction.y *= -1
        elif self.pos.y*SCALE > bounds_rect.bottom:
            self.pos.y = bounds_rect.bottom/SCALE
            self.direction.y *= -1


    def social_move(self, time_passed):
        # force is computed over neighbors with 0.5m radius (= 0.5*100 px)
        self._social_neighbors = self.game.get_agent_neighbors(self, (0.5*SCALE))

        # compute the forces
        self._social_force = self._compute_social_force()
        self._desired_force = self._compute_desired_force()
        self._obstacle_force = self._compute_obstacle_force()
        self._lookahead_force = self._compute_lookahead_force()


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
        if self._counter > (randint(200, 300) / 1000.0):
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
    _waypoints = []
    _waypoint_index = 0


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

    @property
    def waypoints(self):
        return self._waypoints

    @property
    def next_waypoint(self):
        return self._waypoints[self._waypoint_index]



     

    def _compute_social_force(self):
        social_force = Vector3(0, 0, 0)

        for neighbor in self._social_neighbors:
            force = Vector3(0, 0, 0)

            if not neighbor.id == self.id:
                dist = self.pos.get_distance(neighbor.pos)
                exp_dist = exp(sqrt(dist) - 1)

                # [2cm - 20m] range
                if dist > (0.02 * SCALE) and dist < (20*SCALE):
                    force[0] = (neighbor.pos.x - self.pos.x) / exp_dist
                    force[1] = (neighbor.pos.y - self.pos.y) / exp_dist

                social_force[0] = force[0]
                social_force[1] = force[1]
                social_force[2] = force[2]

        return social_force



    def _compute_desired_force(self):
        if self.reached_waypoint(self.next_waypoint):
            self._waypoint_index += 1

        # if all waypoints are covered, go back to the beginning
        # this does not take into account birth and death waypoints yet
        if self._waypoint_index == len(self.waypoints):
            self._waypoint_index = 0

        wp_force = self.next_waypoint.force_to(self)

        desired_force = Vector3(0, 0, 0)
        desired_force[0] = wp_force[0] * self.max_speed
        desired_force[1] = wp_force[1] * self.max_speed
        desired_force[2] = wp_force[2] * self.max_speed

        return desired_force


    def _compute_obstacle_force(self):
        obstacle_force = Vector3(0, 0, 0)

        # find the closest obstacle and the closest point on it
        current_distance, current_ppoint = self.game.obstacles[0].agent_distance(self)
        for obstacle in self.game.obstacles:
            other_distance, other_point = obstacle.agent_distance(self)

            if other_distance < current_distance:
                current_distance, current_ppoint = other_distance, other_point

        # compute the direction of the force
        obstacle_force[0] = -(self.x - current_ppoint[0]) / exp(current_distance - 1)
        obstacle_force[1] = -(self.y - current_ppoint[1]) / exp(current_distance - 1)
        # obstacle_force[0] = -(self.x - current_ppoint[0]) * self.max_speed
        # obstacle_force[1] = -(self.y - current_ppoint[1]) * self.max_speed

        return obstacle_force

    def _compute_lookahead_force(self):
        lookahead_force = Vector3(0, 0, 0)
        return lookahead_force


