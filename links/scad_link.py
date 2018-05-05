"""Link generator.
"""
import os
from sys import platform

import numpy as np

from links.link import LinkGenerator


class ScadLinkGenerator(LinkGenerator):

    def __init__(self,
                 name,
                 mass_range,
                 lateral_friction_range,
                 spinning_friction_range,
                 inertia_friction_range,
                 scale_range,
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

        # Generate mesh use OpenScad.
        data['scad_type'] = 'cube'  # TODO
        data['filename'] = self.run_openscad(path, data)

        return data

    def run_openscad(self, path, data):
        """Run OpenScad command.
        """
        scad_filename = os.path.join(path, '%s.scad' % (self.name))
        stl_filename = os.path.join(path, '%s.stl' % (self.name))
        obj_filename = os.path.join(path, '%s.obj' % (self.name))
        output_filename = os.path.join(path, '%s' % (self.name))

        self.generate_scad(scad_filename, data)

        command = 'openscad -o {:s} {:s}'.format(stl_filename, scad_filename)
        os.system(command)

        if platform == 'linux' or platform == 'linux2':
            meshconv_bin = './bin/meshconv_linux'
        elif platform == 'darwin':
            meshconv_bin = './bin/meshconv_osx'
        elif platform == 'win32':
            meshconv_bin = './bin/meshconv.exe'
        else:
            raise ValueError

        command = '{:s} -c obj -tri -o {:s} {:s}'.format(
                meshconv_bin, output_filename, stl_filename)
        os.system(command)

        return obj_filename

    def generate_scad(self, filename, data):
        """
        """
        if data['scad_type'] == 'cube':
            scad = 'cube([{:f}, {:f}, {:f}]);'.format(
                    data['scale_x'],
                    data['scale_y'],
                    data['scale_z'])
        # elif data['scad_type'] == 'cylinder':
        #     'cylinder([{:f}, {:f}, {:f}]);'.format(
        #             data['scale_z'],
        #             data['scale_x'],
        #             data['scale_y'])
        else:
            pass

        with open(filename, 'w') as f:
            f.write(scad)
