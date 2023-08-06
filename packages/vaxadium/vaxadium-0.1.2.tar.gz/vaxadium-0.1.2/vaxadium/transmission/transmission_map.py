"""
Created on 22 Oct 2018

@author: Timothy Spain
"""
import logging

import numpy as np
import scipy.interpolate

logger = logging.getLogger(__name__)


class TransmissionMap(object):
    """
    A class to hold the component transmission maps for XPDF processing
    """

    def __init__(self, params):
        """
        Constructor
        """
        self.n_pixels = params.get("n_pixels", [20, 20])
        self.n_voxels = params.get("n_voxels", 64)

    def calculate_single_map(self, scatterer, attenuator, beam, target_directions):
        # The output array has the same shape as the first two dimensions of the
        # target_directions array
        transmission_map = np.array(
            target_directions[:, :, 0], dtype="f8"
        )  # dean is not sure what this is for?

        itery = np.ndenumerate(transmission_map)

        for (i, j), t in itery:
            if j == 0:
                logger.debug("Tracing pixel ({},{})".format(i, j))
            transmission_map[i, j] = scatterer.calculate_mean_transmission(
                attenuator, beam, target_directions[i, j]
            )

        return transmission_map

    def calculate(self, components, beam, detector):
        n_voxels = self.n_voxels
        logger.info("starting calculation with {} voxels".format(n_voxels))
        n_components = len(components)
        if hasattr(self, "n_pixels"):
            tmaps = np.zeros((n_components, n_components), dtype=(float, self.n_pixels))
        else:
            tmaps = np.zeros(
                (n_components, n_components), dtype=(float, detector.n_pixels)
            )
        for i_scatterer in range(n_components):
            scatterer = components[i_scatterer].get_scatterer(n_voxels)
            for j_attenuator in range(n_components):
                attenuator = components[j_attenuator]
                logger.debug("Asking for directions")
                if hasattr(self, "n_pixels"):
                    logger.debug("Decimating")

                    dirs = self.decimate_dirs(detector)
                else:
                    logger.info("Using full size")
                    dirs = detector.get_target_directions()
                logger.debug("Calculating map {}, {}".format(i_scatterer, j_attenuator))
                tmaps[i_scatterer, j_attenuator] = self.calculate_single_map(
                    scatterer, attenuator, beam, dirs
                )

        if tmaps[0, 0].shape != detector.n_pixels:
            logger.info("Upscaling")
            tmaps = self.upscale_maps(tmaps, detector.n_pixels)
        return tmaps

    def decimate_dirs(self, detector):
        (raw_x, raw_y) = detector.n_pixels
        self.dx = raw_x * 1.0 / self.n_pixels[0]
        self.dy = raw_y * 1.0 / self.n_pixels[1]

        decimated = np.zeros(self.n_pixels, dtype=(float, 3))
        for i in range(self.n_pixels[0]):
            for j in range(self.n_pixels[1]):
                x = (i + 0.5) * self.dx
                y = (j + 0.5) * self.dy
                posn = detector.get_pixel_position(int(x), int(y))
                decimated[i, j, :] = posn / np.linalg.norm(posn)

        return decimated

    def upscale_maps(self, maps, target_shape):
        # x and y coordinates of the decimated points
        x = np.arange(self.dx / 2, target_shape[0], self.dx)
        y = np.arange(self.dy / 2, target_shape[1], self.dy)

        new_x = np.arange(target_shape[0])
        new_y = np.arange(target_shape[1])
        XX, YY = np.meshgrid(new_x, new_y)
        n_comp = maps.shape[0]
        large_maps = np.zeros((n_comp, n_comp), dtype=(float, target_shape))

        for i in range(n_comp):
            for j in range(n_comp):
                # "this might be overkill, it might just be...... slow" - TS
                spline = scipy.interpolate.RectBivariateSpline(x, y, maps[i, j])
                large_maps[i, j] = spline.ev(YY, XX)
        return large_maps
