"""Body generator.
"""

import abc


class Body(object):
    """Body generator.
    """

    __metaclass__ = abc.ABCMeta

    def __init__(self, name, obj_paths=None):
        """Initialize.

        Args:
            name: The name of the body URDF file.
            obj_paths: If None, use OpenScad to gnerate objects; otherwise
                sample objects from obj_paths.
        """
        pass

    @abc.abstractmethod
    def generate(self, path):
        """Generate a body.

        Args:
            path: The folder to save the URDF and OBJ files.
        """
        pass
