"""Link generator.
"""
import os

import numpy as np


class LinkGenerator(object):

    def __init__(self,
                 name,
                 mass_range,
                 lateral_friction_range,
                 spinning_friction_range,
                 inertia_friction_range,
                 scale_range,
                 mesh_paths,
                 ):
        """Initialize.
        """
        with open('templates/link.xml', 'r') as f:
            self.template = f.read()

        self.name = name
        self.mass_range = mass_range
        self.lateral_friction_range = lateral_friction_range
        self.spinning_friction_range = spinning_friction_range
        self.inertia_friction_range = inertia_friction_range
        self.scale_range = scale_range
        self.mesh_paths = mesh_paths

    def generate(self, path=None):
        """Generate a link.

        The center of mass of each mesh should be aligned with the origin.

        Args:
            path: The folder to save the URDF and OBJ files.

        Returns:
            data: Dictionary of the link attributes.
        """
        data = dict()

        data['name'] = self.name

        # Set contact.
        data['mass'] = np.random.uniform(*self.mass_range)

        # Set inertial.
        data['lateral_friction'] = np.random.uniform(
                *self.lateral_friction_range)
        data['spinning_friction'] = np.random.uniform(
                *self.spinning_friction_range)
        data['inertia_scaling'] = np.random.uniform(
                *self.inertia_friction_range)

        # Set mesh.
        data['x'] = 0
        data['y'] = 0
        data['z'] = 0
        data['roll'] = 0
        data['pitch'] = 0
        data['yaw'] = 0
        data['scale_x'] = np.random.uniform(*self.scale_range[0])
        data['scale_y'] = np.random.uniform(*self.scale_range[1])
        data['scale_z'] = np.random.uniform(*self.scale_range[2])

        # Choose mesh.
        mesh_file = np.random.choice(self.mesh_paths)
        data['filename'] = os.path.join(path, '%s.obj' % (self.name))
        command = 'cp {:s} {:s}'.format(mesh_file, data['filename'])
        os.system(command)

        return data

    def convert_data_to_urdf(self, data):
        """Get the urdf text of the link.

        Args:
            data: Dictionary of the link attributes.

        Returns:
            The text of the link data in the URDF format.
        """
        return self.template.format(**data)
