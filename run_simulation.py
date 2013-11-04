
from crowdsim import Simulation






def start_main_simulation(params):
    sim = Simulation(params)
    sim.run()


if __name__ == '__main__':
    params = {
                'screen_width': 800,
                'screen_height': 800,
                'cell_width': 10
            }
    start_main_simulation(params)