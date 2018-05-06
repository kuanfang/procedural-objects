"""Link generator through OpenScad.
"""
import abc
import os
from sys import platform

import numpy as np

from links.link import Link


class ScadLink(Link):
    """Generate link with OpenScad.

    http://www.openscad.org/cheatsheet/index.html
    """

    def __init__(self,
                 name,
                 size_range,
                 mass_range,
                 lateral_friction_range,
                 spinning_friction_range,
                 inertia_friction_range,
                 ):
        """Initialize.

        Args:
            name: Name of the link.
            size_range: The range of the shape size as a numpy array of [3, 2].
            mass_range: The range of the mass of the link.
            lateral_friction_range: The range of the lateral friction.
            spinning_friction_range: The range of the spinning friction.
            inertia_friction_range: The range of the inertia friction.
        """
        with open('templates/link.xml', 'r') as f:
            self.template = f.read()

        self.name = name
        self.size_range = size_range
        self.mass_range = mass_range
        self.lateral_friction_range = lateral_friction_range
        self.spinning_friction_range = spinning_friction_range
        self.inertia_friction_range = inertia_friction_range

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
        data['size_x'] = np.random.uniform(*self.size_range[0])
        data['size_y'] = np.random.uniform(*self.size_range[1])
        data['size_z'] = np.random.uniform(*self.size_range[2])
        data['scale_x'] = 1
        data['scale_y'] = 1
        data['scale_z'] = 1

        # Generate mesh use OpenScad.
        data['filename'] = self.run_openscad(path, data)

        return data

    def run_openscad(self, path, data):
        """Run OpenScad command.

        Args:
            path: The folder to save the URDF and OBJ files.
            data: The data dictionary.

        Returns:
            obj_filename: The filename of the OBJ file.
        """
        # Set filenames.
        scad_filename = os.path.join(path, '%s.scad' % (self.name))
        stl_filename = os.path.join(path, '%s.stl' % (self.name))
        obj_filename = os.path.join(path, '%s.obj' % (self.name))
        output_filename = os.path.join(path, '%s' % (self.name))

        # Run OpenScad.
        scad = self.generate_scad(data)

        with open(scad_filename, 'w') as f:
            f.write(scad)

        command = 'openscad -o {:s} {:s}'.format(stl_filename, scad_filename)
        os.system(command)

        # Convert the generated STL file to OBJ file.
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

        # Return.
        return obj_filename

    @abc.abstractmethod
    def generate_scad(self, data):
        """Randomly generate the OpenScad description data.

        Args:
            data: The data dictionary.

        Returns:
            scad: The description data.
        """
        raise NotImplementedError


class ScadCubeLink(ScadLink):
    """Generate cuboids with OpenScad.

    https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Primitive_Solids#cube
    """

    def generate_scad(self, data):
        """Randomly generate the OpenScad description data.

        Args:
            data: The data dictionary.

        Returns:
            scad: The description data.
        """
        scad = 'cube([{x:f}, {y:f}, {z:f}], center=true);'.format(
                x=data['size_x'], y=data['size_y'], z=data['size_z'])

        return scad
