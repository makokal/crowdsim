
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

from collections import defaultdict
from pprint import pprint



class SceneIO(object):
    """ Simulation scene IO mechanism """
    def __init__(self, scene_file=None):
        """ Creat a scene io manager (load a new scene by default)

        scene_file:
            The filename of the scene (eg. scene.xml)

        """
        self._scene_file = scene_file
        self._tree = ET.parse(self._scene_file).getroot()
        self._dict = self._etree_to_dict2(self._tree)
        pprint(self._dict)


    def load_scene(self, scene_file):
        self._tree = ET.parse(self._scene_file).getroot()
        self._dict = self._etree_to_dict2(self._tree)


    def get_agents(self):
        return self._dict['simulation']['agent']


    def get_obstacles(self):
        return self._dict['simulation']['obstacle']


    def get_waypoints(self):
        return self._dict['simulation']['waypoint']


    def get_parameters(self):
        return self._dict['simulation']['parameters']


    def save_scene(self, filename):
        # TODO - Check filename validity
        tree = ET.ElementTree(self._tree)
        tree.write(filename)


    def _etree_to_dict(self, element):
        node = dict()

        text = getattr(element, 'text', None)
        if text is not None:
            node['text'] = text

        node.update(element.items()) # element's attributes

        child_nodes = {}
        for child in element: # element's children
            child_nodes.setdefault(child, []).append( self._etree_to_dict(child) )

        # convert all single-element lists into non-lists
        for key, value in child_nodes.items():
            if len(value) == 1:
                 child_nodes[key] = value[0]

        node.update(child_nodes.items())

        return node

    def _etree_to_dict2(self, t):
        """ _etree_to_dict(t)
            Convert an ET tree to python dict
        """
        d = {t.tag: {} if t.attrib else None}
        children = list(t)
        if children:
            dd = defaultdict(list)
            for dc in map(self._etree_to_dict2, children):
                for k, v in dc.iteritems():
                    dd[k].append(v)
            d = {t.tag: {k:v[0] if len(v) == 1 else v for k, v in dd.iteritems()}}
        if t.attrib:
            # d[t.tag].update(('@' + k, v) for k, v in t.attrib.iteritems())
            d[t.tag].update((k, v) for k, v in t.attrib.iteritems())
        if t.text:
            text = t.text.strip()
            if children or t.attrib:
                if text:
                  d[t.tag]['#text'] = text
            else:
                d[t.tag] = text
        return d





        