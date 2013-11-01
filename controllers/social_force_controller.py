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
        agent._velocity.x += delta_time * forces[0]
        agent._velocity.y += delta_time * forces[1]

        # check is resulting speed is beyond maximum speed
        if agent._velocity.get_length() > agent._vmax:
            agent._velocity.x = (agent._velocity.normalized().x) * agent._vmax
            agent._velocity.y = (agent._velocity.normalized().y) * agent._vmax

        # update positions and velocities
        displacement = agent._velocity * delta_time
        agent.prev_pos = vec2d(agent.position)
        agent.position += displacement



    def info(self):
        return 'Social Force Controller'