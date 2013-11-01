from random import randint

from controllers import Controller
from utils import vec2d


class RandomController(Controller):
    """A Random controller, which drives the agents anywhere in the scene"""
    
    def __init__(self, environment):
        self.environment = environment

    def drive_single_step(self, agent, delta_time):
        """ drive_single_step
        Drive the agent over a single simulation step
        """
        self._change_direction(agent, delta_time / 1000.0)
        displacement = vec2d(    
            agent._direction.x * agent._vmax * (delta_time),
            agent._direction.y * agent._vmax * (delta_time))            
        agent.prev_pos = vec2d(agent._position)
        agent.position += displacement


    def info(self):
        return 'Random Controller'


    _counter = 0
    
    def _change_direction(self, agent, delta_time):
        """ Turn by 45 degrees in a random direction once per
            0.05 to 0.3 seconds.
        """

        # agent._direction.rotate(45 * randint(-1, 1))

        # print delta_time*2000.0, (randint(50, 300) / 1000.0)
        self._counter += delta_time*2000.0
        if self._counter > (randint(50, 300) / 1000.0):
            agent._direction.rotate(45 * randint(-1, 1))
            self._counter = 0