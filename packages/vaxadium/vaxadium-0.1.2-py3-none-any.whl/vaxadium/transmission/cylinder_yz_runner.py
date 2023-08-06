"""
Created on 15 Mar 2019

@author: Timothy Spain
"""
import matplotlib.pyplot as plt

from .cylinder_yz import CylinderYZ

if __name__ == "__main__":
    outer = CylinderYZ({"r_inner": 50, "r_outer": 51, "n_voxels": 100})
    inner = CylinderYZ({"r_inner": 0, "r_outer": 50, "n_voxels": 100})

    #     for (coords, vol) in inner.coordinates_volume():
    #         print(coords)

    for (z, y), vol in outer.coordinates_volume():
        plt.scatter(y, z, vol, "red")
    for (z, y), vol in inner.coordinates_volume():
        plt.scatter(y, z, vol, "blue")

    plt.show()
