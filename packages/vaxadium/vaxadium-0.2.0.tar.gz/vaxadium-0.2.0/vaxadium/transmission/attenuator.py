"""
Created on 22 Oct 2018

@author: Timothy Spain
"""
import math

import numpy as np
import xraylib

from ..constants import KEYS
from .scatterer import CylindricalScatterer


class Attenuator(object):
    """
    An attenuator, currently cylindrical geometry only.
    Incident beam toward +ve z direction
    Cylinder aligned along the x axis
    Concentric, origin centred
    """

    def __init__(self, params, sample_number=""):
        """
        Constructor
        """
        self.__r_inner__ = params[KEYS.SAMPLEn_RINNER.format(sample_number)]  # cm
        self.__r_outer__ = params[KEYS.SAMPLEn_ROUTER.format(sample_number)]  # cm
        self.material = params[KEYS.SAMPLEn_CHEMICAL_FORMULA.format(sample_number)]
        self.density = params[KEYS.SAMPLEn_DENSITY.format(sample_number)]  # g/cm³
        self.volume_fraction = params[
            KEYS.SAMPLEn_VOLUME_FRACTION.format(sample_number)
        ]
        self.mu = None
        if KEYS.BEAM in params.keys():
            self.add_beam(params[KEYS.BEAM])

    def __eq__(self, other):
        if type(other) is type(self):
            return all(
                (
                    self.__r_inner__ == other.__r_inner__,
                    self.__r_outer__ == other.__r_outer__,
                    self.material == other.material,
                    self.density == other.density,
                    self.volume_fraction == other.volume_fraction,
                    self.mu == other.mu,
                )
            )
        else:
            return False

    def __repr__(self):
        return object.__repr__(self) + str(self.__dict__)

    def add_beam(self, beam):
        sigma = xraylib.CS_Total_CP(self.material, beam.energy)  # cm²/g
        self.mu = sigma * self.density * self.volume_fraction  # 1/cm

    """
    Returns the transmission of the beam entering along beam_direction (numpy
    unit 3-vector), being scattered at scattering_coords (3-vector) in the
    direction scattering_direction (numpy unit 3-vector)
    """

    def transmission(self, scattering_coords, beam_direction, scattering_direction):
        incoming_transmission = self.half_trans(scattering_coords, beam_direction)
        # reverse the direction of the outgoing beam
        scattering_direction = np.array(scattering_direction)
        outgoing_transmission = self.half_trans(
            scattering_coords, scattering_direction * -1
        )

        return incoming_transmission * outgoing_transmission

    """
    Returns the transmission through a material with absorption mu (1/cm) from
    coords (numpy 3-vector) in the direction (numpy unit 3-vector)
    """

    def half_trans(self, coords, direction):
        direction_2d = np.copy(direction)
        direction_2d[0] = 0.0
        direction_2d /= np.linalg.norm(direction_2d)
        x = direction[0]
        coords_2d = np.copy(coords)
        coords_2d[0] = 0.0

        path_length = self.path_length_2d(coords_2d, direction_2d)
        sec_factor = 1 / (1 - x**2) ** 0.5
        path_length *= sec_factor  # path length increases as the secant of
        # the out-of-plane scattering angle

        return math.exp(-self.mu * path_length)

    """
        Path length from infinity to the specified point in the given direction.
    """

    def path_length_2d(self, coords, direction):
        # Rotate so that the direction is (0, 0, 1) assumes direction is normalized
        m = np.array(
            [
                [1.0, 0.0, 0.0],
                [0.0, direction[2], -direction[1]],
                [0.0, direction[1], direction[2]],
            ]
        )

        # Rotate and covert to two dimensions
        ny_coords = np.matmul(m, coords)[1:3]
        ny_coords[0] = math.fabs(ny_coords[0])

        return self.path_length_canon(ny_coords)

    """
    Path length for a beam directed along (0, 1)
    """

    def path_length_canon(self, coords):
        swap_coords = coords[::-1]

        positive_path_length = Attenuator.semicircular_path(
            self.__r_outer__, swap_coords
        )
        negative_path_length = Attenuator.semicircular_path(
            self.__r_inner__, swap_coords
        )

        return positive_path_length - negative_path_length
        # Use path length through a semi-circle

    @staticmethod
    def semicircular_path(radius, coords):
        x = coords[0]
        y = math.fabs(coords[1])
        try:
            bdy = math.sqrt(radius**2 - y**2)
        except ValueError:
            pass  # We can accept taking the square root of a negative number
        if np.dot(coords, coords) > radius**2:
            if x < 0 or y > radius:
                return 0.0
            else:
                return 2.0 * bdy

        return x + bdy

    def get_scatterer(self, n_voxels):
        return CylindricalScatterer(
            {
                "r_inner": self.__r_inner__,
                "r_outer": self.__r_outer__,
                "n_elements": n_voxels,
            }
        )
