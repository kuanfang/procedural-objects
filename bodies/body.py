"""Body generator.
"""

import abc


class Body(object):
    """Body generator.
    """

    __metaclass__ = abc.ABCMeta

    def __init__(self, obj_paths=None, name='body.urdf'):
        """
        """
        pass

    @abc.abstractmethod
    def generate(self, path):
        """Generate a body.

        Args:
            path: The folder to save the URDF and OBJ files.
        """
        pass
