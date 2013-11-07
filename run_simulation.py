
from crowdsim import Simulation
from iosystem import SceneIO

from pprint import pprint


def start_main_simulation(params):
    sim = Simulation(params)
    sim.run()


if __name__ == '__main__':
    sio = SceneIO('scenes/simple_room.xml')
    # pprint(sio.get_parameters())
    
    start_main_simulation(sio.get_parameters())