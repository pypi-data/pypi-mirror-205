"""
Created on 15 Feb 2019

@author: Timothy Spain, timothy.spain@diamond.ac.uk
"""
import math

import numpy as np

from .illuminated_yz import IlluminatedYZ


class Scatterer(object):
    """
    Provides a scatterer as a set of voxels
    """

    def __init__(self, params):
        """
        Generic constructor
        """

    """
    Calculates the mean transmission in the given direction for the scatterer
    as attenuated by the attenuator.
    """

    def calculate_mean_transmission(self, attenuator, beam, scattering_direction):
        print("WTF why am I being called?")
        return 1.0

    @staticmethod
    def round_up_to_2(x):
        log = math.ceil(math.log(x, 2))
        return 2**log


class CylindricalScatterer(Scatterer):
    """
    Provides a set of voxels describing a (hollow) cylindrical scatterer
    """

    def __init__(self, params):
        """
        Cylindrical scatterer. Takes an inner ("r_inner") and an outer ("r_outer")
        radius, and a target number of voxels ("n_elements").
        """
        self.inner = params["r_inner"]
        self.outer = params["r_outer"]
        #         self.density = params["density"]
        n_voxels = params["n_elements"]
        # Round the number of voxels up to the next power of 2
        self.n_voxels = Scatterer.round_up_to_2(n_voxels)

    def calculate_mean_transmission(self, attenuator, beam, scattering_direction):
        """
        import matplotlib.pyplot as plt
        from mpl_toolkits.mplot3d import Axes3D
        fig1=plt.figure()
        ax1 = fig1.add_subplot(111, projection='3d')
        for ((y, z), volume) in yz.coordinates_volume():
            ax1.scatter(y,z,volume)
        """

        yz = IlluminatedYZ(
            {
                "r_inner": self.inner,
                "r_outer": self.outer,
                "b": beam.b,
                "n_voxels": self.n_voxels,
            }
        )

        transmission_acc = 0.0
        volume_acc = 0.0

        for (y, z), volume in yz.coordinates_volume():
            coords = np.array([0.0, y, z])
            x_length = beam.beam_x(coords[1])
            d_volume = volume * x_length
            if d_volume == 0.0:
                continue
            transmission = attenuator.transmission(
                coords, beam.direction, scattering_direction
            )
            transmission_acc += transmission * d_volume
            volume_acc += d_volume

        return transmission_acc / volume_acc
