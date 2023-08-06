"""
Created on 7 Nov 2018

@author: Timothy Spain
"""
import math

import numpy as np
import xraylib

from ..constants import KEYS


class Detector(object):
    """
    Detector pixel locations in 3d space, pixel solid angle and general parameters
    """

    def __init__(self, params):
        """
        Constructor
        """
        self.apply_params(params)

    def __repr__(self):
        return object.__repr__(self) + str(self.__dict__)

    def apply_params(self, params):
        # Detector distance in mm
        if KEYS.DETECTOR_DISTANCE in params:
            self.distance = params[KEYS.DETECTOR_DISTANCE]

        # Pixel size in mm
        if KEYS.PIXEL_SIZES in params:
            self.pixel_size = params[KEYS.PIXEL_SIZES]

        # Number of pixels in x and y
        if KEYS.PIXEL_NUMBERS in params:
            self.n_pixels = params[KEYS.PIXEL_NUMBERS]

        # Detector origin as a three-element numpy array
        if KEYS.DETECTOR_ORIGIN in params:
            self.origin = np.array(params[KEYS.DETECTOR_ORIGIN])

        # Basis vectors: uk is the normal, pointing out of the sensitive side
        # of the detector plane
        if KEYS.DETECTOR_UK in params:
            self.uk = np.array(params[KEYS.DETECTOR_UK])
        # ui is the direction of increasing x pixel index
        if KEYS.DETECTOR_UI in params:
            self.ui = np.array(params[KEYS.DETECTOR_UI])

        if hasattr(self, "ui") and hasattr(self, "uk"):
            self.calculate_uj()

        # Detector thickness in mm
        if KEYS.DETECTOR_THICKNESS in params:
            self.thickness = params[KEYS.DETECTOR_THICKNESS]

        # Detector material in a format xraylib understands
        if KEYS.DETECTOR_MATERIAL in params:
            self.material = params[KEYS.DETECTOR_MATERIAL]

        # Detector material density in g/cm³
        if KEYS.DETECTOR_DENSITY in params:
            self.density = params[KEYS.DETECTOR_DENSITY]

    @property
    def sensor(self):
        sensor = {}
        sensor[KEYS.DETECTOR_MATERIAL] = self.material
        sensor[KEYS.DETECTOR_THICKNESS] = self.thickness
        sensor[KEYS.DETECTOR_DENSITY] = self.density
        return sensor

    # Return the lab-frame position of the origin (top-left) of pixel i, j
    # Fractional indices can be used to obtain other points in the pixel
    def get_pixel_position(self, i, j):
        if hasattr(self, "uj"):
            self.calculate_uj()
        return (
            self.origin
            + i * self.pixel_size[0] * self.ui
            - j * self.pixel_size[1] * self.uj
        )

    # The solid angle projected by the pixel at position i, j
    def get_solid_angle(self, i, j):
        position = self.get_pixel_position(math.trunc(i) + 0.5, math.trunc(j) + 0.5)
        distance = np.sqrt(position.dot(position))
        face_on_solid_angle = self.pixel_size[0] * self.pixel_size[1] / distance**2
        solid_angle = face_on_solid_angle * self.angular_projection_from_position(
            position
        )
        return solid_angle

    # Calculate the uj unit vector from ui and uk
    def calculate_uj(self):
        self.uj = np.cross(self.uk, self.ui)

    # Angular projection of an element parallel to the detector at location (i, j)
    def angular_projection(self, i, j):
        position = self.get_pixel_position(math.trunc(i) + 0.5, math.trunc(j) + 0.5)
        return self.angular_projection_from_position(position)

    # Angular projection of an element parallel to the detector at the given vector
    # position
    def angular_projection_from_position(self, position):
        distance = np.sqrt(position.dot(position))
        angular_projection = (
            -position.dot(self.uk) / distance
        )  # negate because uk points out of the detection plane
        return angular_projection

    # Path length of a ray passing through the detector at this point, having been
    # scattered at the origin
    def detector_thickness_from_origin(self, i, j):
        angular_projection = self.angular_projection(i, j)
        return self.thickness / angular_projection

    # Areal density (g/cm²) of detector material encountered by a ray scattered
    # from the origin to detector coordinates i,j
    def detector_projected_areal_density_from_origin(self, i, j):
        return self.density * self.detector_thickness_from_origin(i, j) / 10

    # Transmission of the detector at the given energy (keV)
    def pixel_transmission_from_origin(self, i, j, energy):
        cross_section = xraylib.CS_Photo_CP(self.material, energy)
        transmission = math.exp(
            -cross_section * self.detector_projected_areal_density_from_origin(i, j)
        )
        return transmission

    def transmission_from_origin(self, energy):
        trans = np.zeros(self.n_pixels, dtype=float)
        for i in range(self.n_pixels[0]):
            for j in range(self.n_pixels[1]):
                trans[j, i] = self.pixel_transmission_from_origin(i, j, energy)
        return trans

    # Returns an nx × ny × 3 array of the unit length direction of each pixel
    def get_target_directions(self):
        dirs = np.zeros(self.n_pixels, dtype=(float, 3))
        for i in range(self.n_pixels[0]):
            for j in range(self.n_pixels[1]):
                if i % 10 == 0 and j % 10 == 0:
                    print("Directing pixel (", i, ", ", j, ")")
                direc = self.get_pixel_position(i, j)
                dirs[i, j] = direc / np.linalg.norm(direc)

        return dirs

    # returns the Thomson differential scattering cross-section in square electron radii
    def thomson_dscp(self, beam):
        raise NotImplementedError
        re = 2.8179403227e-15  # m
        re_sq = re**2  # m²
        re_sq_b = re_sq / 1e-28  # barns

        thoms = np.zeros(self.n_pixels, dtype=float)
        outth = np.zeros(self.n_pixels, dtype=float)
        for i in range(self.n_pixels[0]):
            for j in range(self.n_pixels[1]):
                direc = self.get_pixel_position(i, j)
                direc /= np.linalg.norm(direc)
                beamward_length = np.dot(beam.direction, direc)
                ttheta = math.acos(beamward_length)
                polarization_parallel = direc - beamward_length
                polarization_parallel /= np.linalg.norm(polarization_parallel)
                # ui is here taken to be the direction of polarization
                phi = math.acos(np.dot(polarization_parallel, self.ui))
                outth[i, j] = phi
                if i == 0 and j == 1:
                    print(direc)
                    print(ttheta)
                    print(polarization_parallel)
                    print(phi)
                thoms[i, j] = xraylib.DCSP_Thoms(ttheta, phi) / re_sq_b

        return thoms, outth
