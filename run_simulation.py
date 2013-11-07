
from crowdsim import Simulation
from iosystem import SceneIO

from pprint import pprint


def start_main_simulation(params):
    sim = Simulation(params)
    sim.run()


if __name__ == '__main__':
    params = {
                'screen_width': 800,
                'screen_height': 600,
                'cell_width': 10
            }


    sio = SceneIO('scenes/simple_room.xml')
    # print sio._dict

    # tree = ET.parse('scenes/simple_room.xml')
    # d = etree_to_dict(tree.getroot())
    pprint(sio._dict['simulation']['agent'])
    pprint(sio._dict['simulation']['obstacle'])
    pprint(sio._dict['simulation']['waypoint'])

    # start_main_simulation(params)