
from random import randint, choice
from math import sin, cos, radians, exp, sqrt

import pygame
from pygame.sprite import Sprite
# from pygame.math import vec2d
from utils import SIM_COLORS, SCALE, SIGN
from utils import euclidean_distance, vec2d


class Agent(Sprite):
    """ A agent sprite that bounces off walls and changes its
        direction from time to time.
    """

    # __slots__ = ('id', 'screen', 'game', 'field', 'image', \
    #             'vmax', 'position', 'velocity', 'acceleration'\
    #             'radius', 'relaxation_time', 'direction', 'neighbors'\
    #             'forces, force_factors', 'waypoints')

    def __init__(self, agent_id, screen, game, agent_image,
            field, init_position, init_direction, max_speed, waypoints,
            radius = 0.2, relaxation_time = 0.5, atype = 0):
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
            
            vmax: 
                maximum agent speed, in (m/s)

            waypoints:
                a list of waypoints for the agent to follow
        """
        Sprite.__init__(self)
        
        self._id  = agent_id
        self.screen = screen
        self.game = game
        self._vmax = max_speed
        self._field = field

        self._radius = radius
        self._relaxation_time = relaxation_time
        self._type = atype
        
        # the current image representing the agent
        self._image = agent_image
        
        # A vector specifying the agent's position on the screen
        self._position = vec2d(init_position)
        self.prev_pos = vec2d(self._position)

        # The direction is a normalized vector
        self._direction = vec2d(init_direction).normalized()
        self._velocity = vec2d(init_direction)
        self._acceleration = vec2d(0.0, 0.0)

        self._waypoints = waypoints
        self._waypoint_index = 0
        self._neighbors = []

        # # default no forces
        self._social_force = vec2d(0.0, 0.0)
        self._desired_force = vec2d(0.0, 0.0)
        self._obstacle_force = vec2d(0.0, 0.0)
        self._lookahead_force = vec2d(0.0, 0.0)


    def draw(self):
        """ 
        Draw the agent onto the screen that is set in the constructor
        """

        self.draw_rect = self._image.get_rect().move(
            (self._position.x*SCALE) - self._image_w / 2, 
            (self._position.y*SCALE) - self._image_h / 2)
        self.screen.blit(self._image, self.draw_rect)

        # draw the forces on the agent
        self.draw_forces()

        # agent horizon
        pygame.draw.circle(self.screen, SIM_COLORS['yellow'], (int(self._position.x*SCALE), int(self._position.y*SCALE)), int(self._radius*SCALE), int(1))


    def draw_forces(self):
        # desired force
        pygame.draw.line(self.screen, SIM_COLORS['red'],
                ((self._position.x*SCALE), (self._position.y*SCALE)),
                ((self._position.x*SCALE) + self.desired_force[0]*SCALE, (self._position.y*SCALE) + self.desired_force[1]*SCALE))

        # social force
        pygame.draw.line(self.screen, SIM_COLORS['green'],
                ((self._position.x*SCALE), (self._position.y*SCALE)),
                ((self._position.x*SCALE) + self.social_force[0]*SCALE, (self._position.y*SCALE) + self.social_force[1]*SCALE))

        # obstacle force
        pygame.draw.line(self.screen, SIM_COLORS['aqua'],
                ((self._position.x*SCALE), (self._position.y*SCALE)),
                ((self._position.x*SCALE) + self.obstacle_force[0]*SCALE, (self._position.y*SCALE) + self.obstacle_force[1]*SCALE))



    def reached_waypoint(self, waypoint):
        """ Check if the agent has reached the given waypoint so we 
            advance to the next one. Reaching means being in the 
            waypoint circle
        """
        if euclidean_distance((self._position.x, self._position.y), waypoint.position) <= waypoint.radius:
            return True
        else:
            return False


    def update(self, time_passed):        
                
        # When the image is rotated, its size is changed.
        self._image_w, self._image_h = self._image.get_size()
        # bounds_rect = self.screen.get_rect().inflate(-self._image_w, -self._image_h)
        bounds_rect = self.game.field_box.get_internal_rect()
        
        if self._position.x*SCALE < bounds_rect.left:
            self._position.x = bounds_rect.left/SCALE
            self._direction.x *= -1
        elif self._position.x*SCALE > bounds_rect.right:
            self._position.x = bounds_rect.right/SCALE
            self._direction.x *= -1
        elif self._position.y*SCALE < bounds_rect.top:
            self._position.y = bounds_rect.top/SCALE
            self._direction.y *= -1
        elif self._position.y*SCALE > bounds_rect.bottom:
            self._position.y = bounds_rect.bottom/SCALE
            self._direction.y *= -1


    def social_move(self, time_passed):
        # force is computed over neighbors with 0.5m radius (= 0.5*100 px)
        self._neighbors = self.game.get_agent_neighbors(self, (0.5*SCALE))

        # compute the forces
        self._social_force = self._compute_social_force()
        self._desired_force = self._compute_desired_force()
        self._obstacle_force = self._compute_obstacle_force()
        self._lookahead_force = self._compute_lookahead_force()



    """ =================================================================  
        Properties and how to compute them
        =================================================================  
    """

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
    def id(self):
        return self._id

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, newpos):
        self._position = newpos

    @property
    def velocity(self):
        return self._velocity

    @property
    def acceleration(self):
        return self._acceleration

    @property
    def next_waypoint(self):
        return self._waypoints[self._waypoint_index]




    def _compute_social_force(self):
        # variables according to Moussaid-Helbing paper
        lambda_importance = 2.0
        gamma = 0.35
        n, n_prime = 2, 3

        social_force = vec2d(0, 0)
        for neighbor in self._neighbors:
            
            # no social force with oneself
            if neighbor.id == self.id:
                continue
            else:
                # position difference
                diff = neighbor.position - self.position
                diff_direction = diff.normalized()

                # velocity difference 
                vel_diff = self.velocity - neighbor.velocity

                # interaction direction t_ij
                interaction_vector = lambda_importance * vel_diff + diff_direction
                interaction_direction = interaction_vector / interaction_vector.get_length()

                # theta (angle between interaction direction and position difference vector)
                theta = interaction_direction.get_angle_between(diff_direction)

                # model parameter B = gamma * ||D||
                B = gamma * interaction_vector.get_length()
                
                theta_rad = radians(theta)
                force_vel_amount = -exp(-diff.get_length() / B - (n_prime * B * theta_rad)**2)
                force_angle_amount = (-1 * SIGN(theta)) * exp(-diff.get_length() / B - (n * B * theta_rad)**2)

                force_vel = force_vel_amount * interaction_direction
                force_angle = force_angle_amount * interaction_direction.left_normal_vector()

                # social_force[0] += force_vel.x + force_angle.x
                # social_force[1] += force_vel.y + force_angle.y

                social_force += force_vel + force_angle

        return social_force

        


    def _compute_desired_force(self):
        if self.reached_waypoint(self.next_waypoint):
            self._waypoint_index += 1

        # if all waypoints are covered, go back to the beginning
        # this does not take into account birth and death waypoints yet
        if self._waypoint_index == len(self._waypoints):
            self._waypoint_index = 0

        wp_force = self.next_waypoint.force_towards(self)

        desired_force = vec2d(0, 0)
        # desired_force[0] = wp_force[0] * self._vmax
        # desired_force[1] = wp_force[1] * self._vmax
        # desired_force[2] = wp_force[2] * self._vmax

        # desired_force[0] = wp_force.x
        # desired_force[1] = wp_force.y

        desired_force = wp_force

        return desired_force


    def _compute_obstacle_force(self):
        obstacle_force = vec2d(0.0, 0.0)

        # find the closest obstacle and the closest point on it
        closest_distance, closest_point = self.game.obstacles[0].agent_distance(self)
        for obstacle in self.game.obstacles:
            other_distance, other_point = obstacle.agent_distance(self)

            if other_distance < closest_distance:
                closest_distance, closest_point = other_distance, other_point
        

        distance = closest_distance - self._radius
        force_amount = exp(-distance)
        min_diffn = (self._position - vec2d(closest_point)).normalized()

        obstacle_force.x = (force_amount * min_diffn).x
        obstacle_force.y = (force_amount * min_diffn).y

        return obstacle_force


    def _compute_lookahead_force(self):
        lookahead_force = vec2d(0, 0)
        return lookahead_force



