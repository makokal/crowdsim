
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


def xmltodict(element):
    if not isinstance(element, ET.Element):
        raise ValueError("must pass xml.etree.ElementTree.Element object")

    def xmltodict_handler(parent_element):
        result = dict()
        for element in parent_element:
            if len(element):
                obj = xmltodict_handler(element)
            else:
                obj = element.text

            if result.get(element.tag):
                if hasattr(result[element.tag], "append"):
                    result[element.tag].append(obj)
                else:
                    result[element.tag] = [result[element.tag], obj]
            else:
                result[element.tag] = obj
        return result

    return {element.tag: xmltodict_handler(element)}


def dicttoxml(element):
    if not isinstance(element, dict):
        raise ValueError("must pass dict type")
    if len(element) != 1:
        raise ValueError("dict must have exactly one root key")

    def dicttoxml_handler(result, key, value):
        if isinstance(value, list):
            for e in value:
                dicttoxml_handler(result, key, e)
        elif isinstance(value, basestring):
            elem = ET.Element(key)
            elem.text = value
            result.append(elem)
        elif isinstance(value, int) or isinstance(value, float):
            elem = ET.Element(key)
            elem.text = str(value)
            result.append(elem)
        elif value is None:
            result.append(ET.Element(key))
        else:
            res = ET.Element(key)
            for k, v in value.items():
                dicttoxml_handler(res, k, v)
            result.append(res)

    result = ET.Element(element.keys()[0])
    for key, value in element[element.keys()[0]].items():
        dicttoxml_handler(result, key, value)
    return result

def xmlfiletodict(filename):
    return xmltodict(ET.parse(filename).getroot())

def dicttoxmlfile(element, filename):
    ET.ElementTree(dicttoxml(element)).write(filename)

def xmlstringtodict(xmlstring):
    return xmltodict(ET.fromstring(xmlstring).getroot())

def dicttoxmlstring(element):
    return ET.tostring(dicttoxml(element))





class SceneIO(object):
    """ Simulation scene IO mechanism """
    def __init__(self, scene_file=None):
        """ Creat a scene io manager (load a new scene by default)

        scene_file:
            The filename of the scene (eg. scene.xml)

        """
        self._scene_file = scene_file
        self._dict = xmlfiletodict(self._scene_file)


    def load_scene(self, scene_file):
        self._scene_file = scene_file
        self._dict = xmlfiletodict(self._scene_file)

        # do the xml magic
        pass


    def save_scene(self, filename):
        # TODO - Check filename validity
        xml_scene = dicttoxml(self._dict)
        tree = ET.ElementTree(xml_scene.getroot())
        tree.write(filename)



        