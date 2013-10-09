from abc import ABCMeta, abstractmethod


class Controller(object):
    """Abstract controller class defining the interface to controllers """
    
    __metaclass__ = ABCMeta

    @abstractmethod
    def drive_single_step(self):
        return 'This method must be overriden'

    @abstractmethod
    def info(self):
        return 'Abstract Class: please override this method'