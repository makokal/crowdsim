from controllers import Controller
from pygame.math import Vector3
from utils import vec2d
from utils import SF_FACTORS


class SocialForceController(Controller):
    """ Social Force Controller 
        Based on the social force model by Helbing et. al. 95
    """

    def __init__(self, environment):
        """ Initialize the controller

            environment:
                The world that the agent lives in (game)
        """
        self.environment = environment


    def drive_single_step(self, agent, delta_time):
        """ drive_single_step
        Drive the agent over a single simulation step
        """

        # print agent.social_force, agent.desired_force, agent.obstacle_force

        # sum up all the forces
        forces = Vector3(0, 0, 0)
        forces[0] = SF_FACTORS.social * agent.social_force[0] + SF_FACTORS.obstacle * agent.obstacle_force[0] + \
                    SF_FACTORS.desired * agent.desired_force[0] + SF_FACTORS.lookahead * agent.lookahead_force[0]
        forces[1] = SF_FACTORS.social * agent.social_force[1] + SF_FACTORS.obstacle * agent.obstacle_force[1] + \
                    SF_FACTORS.desired * agent.desired_force[1] + SF_FACTORS.lookahead * agent.lookahead_force[1]
        forces[2] = SF_FACTORS.social * agent.social_force[2] + SF_FACTORS.obstacle * agent.obstacle_force[2] + \
                    SF_FACTORS.desired * agent.desired_force[2] + SF_FACTORS.lookahead * agent.lookahead_force[2]

        # calculate the velocity based on the acceleration (forces) and momentum
        velocity = Vector3(0, 0, 0)
        momentum = 0.75

        velocity[0] = momentum * velocity[0] + forces[0]
        velocity[1] = momentum * velocity[1] + forces[1]
        velocity[2] = 0.0 # TODO - add z dimension

        # check is resulting speed is beyond maximum speed
        if velocity.length() > agent._vmax:
            velocity[0] = (velocity[0] / velocity.length()) * agent._vmax
            velocity[1] = (velocity[1] / velocity.length()) * agent._vmax
            velocity[2] = (velocity[2] / velocity.length()) * agent._vmax

        # update positions and velocities
        displacement = vec2d(velocity[0] * delta_time, velocity[1] * delta_time)
        agent.prev_pos = vec2d(agent.position)
        agent.position += displacement



    def info(self):
        return 'Social Force Controller'