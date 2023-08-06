"""
Created on 18 Mar 2019

@author: Timothy Spain
"""
import math

import matplotlib.pyplot as plt

from .illuminated_yz import IlluminatedYZ

if __name__ == "__main__":
    b = 25.0
    illyz = IlluminatedYZ({"r_inner": 50.0, "r_outer": 51.0, "b": b, "n_voxels": 256})

    for chi in [50.0, 35.0, 20.0, 5.0]:
        try:
            psi_edge = math.asin(b / chi)
        except ValueError:
            psi_edge = math.pi / 2

    # print(psi_edge)

    outer = IlluminatedYZ({"r_inner": 50, "r_outer": 51, "n_voxels": 100, "b": 50})
    inner = IlluminatedYZ({"r_inner": 0, "r_outer": 50, "n_voxels": 100, "b": 50})

    #     for (coords, vol) in inner.coordinates_volume():
    #         print(coords)

    for (z, y), vol in outer.coordinates_volume():
        plt.scatter(y, z, vol, "red")
    for (z, y), vol in inner.coordinates_volume():
        plt.scatter(y, z, vol, "blue")

    plt.show()
