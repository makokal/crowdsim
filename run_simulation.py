
from crowdsim import Simulation
from iosystem import SceneIO


import xml.etree.ElementTree as ET
from collections import defaultdict
from pprint import pprint


def etree_to_dict(t):
    d = {t.tag: {} if t.attrib else None}
    children = list(t)
    if children:
        dd = defaultdict(list)
        for dc in map(etree_to_dict, children):
            for k, v in dc.iteritems():
                dd[k].append(v)
        d = {t.tag: {k:v[0] if len(v) == 1 else v for k, v in dd.iteritems()}}
    if t.attrib:
        d[t.tag].update(('@' + k, v) for k, v in t.attrib.iteritems())
    if t.text:
        text = t.text.strip()
        if children or t.attrib:
            if text:
              d[t.tag]['#text'] = text
        else:
            d[t.tag] = text
    return d


def start_main_simulation(params):
    sim = Simulation(params)
    sim.run()


if __name__ == '__main__':
    params = {
                'screen_width': 800,
                'screen_height': 600,
                'cell_width': 10
            }


    # sio = SceneIO('scenes/simple_room.xml')
    # print sio._dict

    tree = ET.parse('scenes/simple_room.xml')
    d = etree_to_dict(tree.getroot())
    pprint(d['simulation']['agent'])
    pprint(d['simulation']['obstacle'])
    pprint(d['simulation']['waypoint'])

    # start_main_simulation(params)