"""
Created on 15 Mar 2019

@author: Timothy Spain
"""
import math

from .yz_generator import YZGenerator


class CylinderYZ(YZGenerator):
    """
    A generator yielding (y, z) coordinate pairs
    """

    def __init__(self, params):
        """
        params: inner radius ("r_inner"), outer radius ("r_outer"),
        number of voxels ("n_voxels")
        """

        self.r_inner = params["r_inner"]
        self.r_outer = params["r_outer"]
        n_voxels = params["n_voxels"]

        thickness = self.r_outer - self.r_inner
        wall_ratio = 6.28 * self.r_outer / thickness

        n_voxels = int(YZGenerator.round_up_to_2(n_voxels))
        n_chi = (n_voxels / wall_ratio) ** 0.5
        self.n_chi = int(YZGenerator.round_up_to_2(n_chi))
        if self.n_chi < 1:
            self.n_chi = 1
        self.n_psi_outer = n_voxels / self.n_chi

        self.d_chi = thickness / self.n_chi
        self.d_psi_outer = 2 * math.pi / self.n_psi_outer

    def coordinates_volume(self):
        for i_chi in range(self.n_chi):
            chi = (i_chi + 0.5) * self.d_chi + self.r_inner
            n_psi = int(
                YZGenerator.round_up_to_2(self.n_psi_outer * chi / self.r_outer)
            )
            if n_psi < 4:
                n_psi = 4
            d_psi = 2 * math.pi / n_psi
            for j_psi in range(n_psi):
                psi = j_psi * d_psi
                volume = self.d_chi * chi * d_psi
                yield ((chi * math.sin(psi), chi * math.cos(psi)), volume)
