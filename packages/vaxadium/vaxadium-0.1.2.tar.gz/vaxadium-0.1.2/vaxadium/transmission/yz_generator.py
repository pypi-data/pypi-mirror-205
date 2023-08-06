"""
Created on 15 Mar 2019

@author: Timothy Spain, timothy.spain@diamond.ac.uk
"""
import math


class YZGenerator(object):
    """
    Abstract base class for generators of (y, z) coordinate pairs
    (2-tuple) for traversing scatterers whilst calculating transmission maps.
    Also includes the voxel volume, returns(coords, vol)
    """

    def __init__(self, params):
        """
        Constructor
        """

    def coordinates_volume(self):
        yield ((0.0, 0.0), 0.0)

    @staticmethod
    def round_up_to_2(x):
        log = math.ceil(math.log(x, 2))
        return 2**log
