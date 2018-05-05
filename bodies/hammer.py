"""Hammer generator.
"""
import os

import numpy as np

from bodies.body import BodyGenerator
from links.link import LinkGenerator
from links.scad_link import ScadLinkGenerator
from utils.transformations import matrix3_from_euler


class HammerGenerator(BodyGenerator):

    HEAD_MASS_RANGE = [0.5, 1.0]
    HEAD_SCALE_RANGE = [[0.1, 0.1], [0.1, 0.1], [1, 1]]

    HANDLE_MASS_RANGE = [0.5, 1.0]
    HANDLE_SCALE_RANGE = [[0.1, 0.1], [0.1, 0.1], [1, 1]]

    LATERAL_FRICTION_RANGE = [0.2, 1.0]
    SPINNING_FRICTION_RANGE = [0.2, 1.0]
    INERTIA_FRICTION_RANGE = [0.2, 1.0]

    def __init__(self, mesh_paths=None, name='body.urdf'):
        """Initialize.
        """
        with open('templates/hammer.xml', 'r') as f:
            self.template = f.read()

        if mesh_paths is None:
            self.handle_generator = ScadLinkGenerator(
                     name='handle',
                     mass_range=self.HANDLE_MASS_RANGE,
                     lateral_friction_range=self.LATERAL_FRICTION_RANGE,
                     spinning_friction_range=self.SPINNING_FRICTION_RANGE,
                     inertia_friction_range=self.INERTIA_FRICTION_RANGE,
                     scale_range=self.HANDLE_SCALE_RANGE,
                     )

            self.head_generator = ScadLinkGenerator(
                     name='head',
                     mass_range=self.HEAD_MASS_RANGE,
                     lateral_friction_range=self.LATERAL_FRICTION_RANGE,
                     spinning_friction_range=self.SPINNING_FRICTION_RANGE,
                     inertia_friction_range=self.INERTIA_FRICTION_RANGE,
                     scale_range=self.HEAD_SCALE_RANGE,
                     )
        else:
            self.handle_generator = LinkGenerator(
                     name='handle',
                     mass_range=self.HANDLE_MASS_RANGE,
                     lateral_friction_range=self.LATERAL_FRICTION_RANGE,
                     spinning_friction_range=self.SPINNING_FRICTION_RANGE,
                     inertia_friction_range=self.INERTIA_FRICTION_RANGE,
                     scale_range=self.HANDLE_SCALE_RANGE,
                     mesh_paths=mesh_paths,
                     )

            self.head_generator = LinkGenerator(
                     name='head',
                     mass_range=self.HEAD_MASS_RANGE,
                     lateral_friction_range=self.LATERAL_FRICTION_RANGE,
                     spinning_friction_range=self.SPINNING_FRICTION_RANGE,
                     inertia_friction_range=self.INERTIA_FRICTION_RANGE,
                     scale_range=self.HEAD_SCALE_RANGE,
                     mesh_paths=mesh_paths,
                     )

        self.name = name

    def sample_head_transformation(self, handle_data, head_data):
        """
        """
        rotation = [np.pi/2, 0., 0.]
        transition = [0., 0., 0.5]

        return rotation, transition

    def transform_point(self, point, rotation, transition):
        """
        """
        roll = rotation[0]
        pitch = rotation[1]
        yaw = rotation[2]
        rotation_matrix = matrix3_from_euler(roll, pitch, yaw)

        return rotation_matrix.dot(point) + np.array(transition)

    def generate(self, path):
        """Generate a body.

        Args:
            path: The folder to save the URDF and OBJ files.
        """
        # Generate links.
        handle_data = self.handle_generator.generate(path)
        head_data = self.head_generator.generate(path)

        # Modify links' positions and orientations.
        rotation, transition = self.sample_head_transformation(
                handle_data, head_data)
        center = [head_data['x'], head_data['y'], head_data['z']]
        center = self.transform_point(center, rotation, transition)
        head_data['x'] = center[0]
        head_data['y'] = center[1]
        head_data['z'] = center[2]
        head_data['roll'] = rotation[0]
        head_data['pitch'] = rotation[1]
        head_data['yaw'] = rotation[2]

        # TODO(kuanfang): Random flipping.

        # Genearte the URDF files.
        handle_urdf = self.handle_generator.convert_data_to_urdf(handle_data)
        head_urdf = self.head_generator.convert_data_to_urdf(head_data)
        urdf = self.template.format(
                name=self.name,
                handle_link=handle_urdf,
                head_link=head_urdf,
                handle_name=handle_data['name'],
                head_name=head_data['name'],
                )

        # Write URDF to file.
        urdf_filename = os.path.join(path, 'body.urdf')
        with open(urdf_filename, 'w') as f:
            f.write(urdf)
