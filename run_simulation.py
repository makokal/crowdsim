
from crowdsim import Simulation
from iosystem import SceneIO

from pprint import pprint


def start_main_simulation(params):
    sim = Simulation(params)
    sim.run()


if __name__ == '__main__':
    sio = SceneIO('scenes/simple_room.xml')
    # pprint(sio.get_waypoints())
    
    sim = Simulation(params=sio.get_parameters())
    sim.add_waypoints(waypoint_dict=sio.get_waypoints())
    sim.add_obstacles(obstacle_dict=sio.get_obstacles())
    sim.add_agents(agent_dict=sio.get_agents())

    sim.run()