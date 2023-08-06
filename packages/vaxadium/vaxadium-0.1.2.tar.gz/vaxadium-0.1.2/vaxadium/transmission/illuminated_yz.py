"""
Created on 15 Mar 2019

@author: Timothy Spain, timothy.spain@diamond.ac.uk
"""
import math

from .yz_generator import YZGenerator


class IlluminatedYZ(YZGenerator):
    """
    A generator yielding (y, z) pairs for voxels in an illuminated cylinder
    """

    def __init__(self, params):
        """
        Constructor
        params: inner radius ("r_inner"), outer radius ("r_outer"),
        beam height ("b"), number of voxels ("n_voxels")
        """

        self.r_inner = params["r_inner"]
        self.r_outer = params["r_outer"]
        n_voxels = params["n_voxels"]
        self.b = params["b"]

        thickness = self.r_outer - self.r_inner
        aspect_ratio = self.b / (2.0 * thickness)

        n_voxels = int(YZGenerator.round_up_to_2(n_voxels))
        n_chi = (n_voxels / aspect_ratio) ** 0.5
        self.n_chi = int(YZGenerator.round_up_to_2(n_chi))
        if self.n_chi < 1:
            self.n_chi = 1
        self.n_chi = int(2 * self.n_chi)

        # Plus one to get an on-beam voxel with symmetric limits
        self.n_psi = int(n_voxels / self.n_chi + 1)

        self.d_chi = 2.0 * thickness / self.n_chi

    def coordinates_volume(self):
        chi_0 = self.r_outer
        d_chi = -self.d_chi
        psi_offset = math.pi
        i_chi_offset = 0

        for i_chi in range(self.n_chi):
            if i_chi >= self.n_chi / 2:
                chi_0 = self.r_inner
                d_chi = self.d_chi
                psi_offset = 0.0
                i_chi_offset = -self.n_chi / 2

            chi = (i_chi + 0.5 + i_chi_offset) * d_chi + chi_0
            # psi angle for chi at the beam margins
            try:
                psi_edge = math.asin(self.b / 2 / chi)
            except ValueError:
                psi_edge = math.pi / 2

            d_psi = 2 * psi_edge / self.n_psi
            psi_0 = -(self.n_psi - 1.0) * d_psi / 2 + psi_offset
            for j_psi in range(self.n_psi):
                psi = j_psi * d_psi + psi_0
                volume = self.d_chi * chi * d_psi
                yield ((chi * math.sin(psi), chi * math.cos(psi)), volume)
