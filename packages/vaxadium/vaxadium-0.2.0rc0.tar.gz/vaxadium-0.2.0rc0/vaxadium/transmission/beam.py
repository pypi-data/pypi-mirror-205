"""
Created on 8 Mar 2019

@author: Timothy Spain, timothy.spain@diamond.ac.uk
"""
import logging
import math

import numpy as np

from ..constants import KEYS

logger = logging.getLogger(__name__)


class Beam(object):
    """
    Represents a beam in the context of transmission maps
    """

    def __init__(self, params):
        """
        Extracts 'energy' (in keV) and direction (unit 3-vector) from params
        """
        assert (
            KEYS.PRIMARY_BEAM_ENERGY in params
        ), "primary beam energy must be supplied in params"
        assert (
            KEYS.PRIMARY_BEAM_DIRECTION in params
        ), "primary beam direction must be supplied in params"
        assert (
            KEYS.PRIMARY_BEAM_HALF_DIMENSIONS in params
        ), "primary beam dimension must be supplied in params"
        self.energy = params[KEYS.PRIMARY_BEAM_ENERGY]
        self.direction = np.array(params[KEYS.PRIMARY_BEAM_DIRECTION], dtype="float")
        if KEYS.ATTENUATOR_TRANSMISSION in params:
            self.normalisation = params[KEYS.ATTENUATOR_TRANSMISSION]
        else:
            self.normalisation = 1.0
        if (
            KEYS.PRIMARY_BEAM_ELLIPTICAL in params
            and params[KEYS.PRIMARY_BEAM_ELLIPTICAL]
        ):
            self.beam_x = self.elliptical_beam_x
        else:
            self.beam_x = self.rectangular_beam_x
        (self.a, self.b) = params[KEYS.PRIMARY_BEAM_HALF_DIMENSIONS]

    def __eq__(self, other):
        if type(self) is type(other):
            a = self.a == other.a
            b = self.b == other.b
            e = self.energy == other.energy
            d = all(self.direction == other.direction)
            bools = (a, b, e, d)
            logger.debug("comparison of {} and {} --> {}".format(self, other, bools))
            return all(bools)
        else:
            return False

    def elliptical_beam_x(self, y):
        if y < self.b:
            x = 2 * self.a * math.sqrt(1 - y**2 / self.b**2)
        else:
            x = 0.0
        return x

    def rectangular_beam_x(self, y):
        if math.fabs(y) < self.b:
            x = 2 * self.a
        else:
            x = 0.0
        return x
