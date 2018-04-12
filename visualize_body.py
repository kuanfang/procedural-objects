#!/usr/bin/env python

"""Load a body to the simulation.
"""

import argparse
import os

import pybullet


def parse_args():
    """Parse arguments.

    Returns:
        args: The parsed arguments.
    """
    parser = argparse.ArgumentParser()

    parser.add_argument(
            '--input',
            dest='input_path',
            type=str,
            default=None,
            help='The path to the URDF file.')

    args = parser.parse_args()

    return args


def main():
    args = parse_args()


    pybullet.connect(pybullet.GUI)
    pybullet.resetSimulation()
    pybullet.setRealTimeSimulation(0)
    pybullet.setTimeStep(1e-2)

    pybullet.loadURDF(
            fileName=args.input_path,
            basePosition=[0, 0, 0],
            baseOrientation=[0, 0, 0, 1],
            useFixedBase=True,
            )

    while(1):
        pybullet.stepSimulation()


if __name__ == '__main__':
    main()

