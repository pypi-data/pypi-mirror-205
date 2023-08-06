"""
Created on 22 Oct 2018

@author: Timothy Spain
"""
import math


class Direction(object):
    """
    A class to convert between coordinates and angular scattering directions
    """

    def __init__(self, params):
        """
        Constructor
        """
        self.__x__ = (0.0, 0.0, 1.0)

    def set_x(self, x):
        self.__x__ = tuple(x)

    # Set direction from
    def set_tth_phi(self, tth, phi):
        z = math.cos(tth)
        rho = math.sin(tth)
        self.__x__ = (rho * math.cos(phi), rho * math.sin(phi), z)

    def get_gamma_deltaprime(self):
        return (
            math.atan2(self.__x__[0], self.__x__[2]),
            math.atan2(self.__x__[1], self.__x__[2]),
        )
