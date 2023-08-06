"""
Created on 18 Apr 2019

@author: Timothy Spain
9th Nov 2020: this produces something that looks a lot like gudrun <F**2>
"""
import math

import numpy as np
import xraylib

from vaxadium.configuration import FORMFACTORKEYS, VaxadiumConfigurationError


def sum_of_f2(q, material, mode="sum_of_squares"):
    atom_data = xraylib.CompoundParser(material)
    sum_squared_fs = 0 * q
    sum_fs = 0 * q
    q_xraylib = q / (4 * math.pi)
    # Iterate over atoms
    for i in range(atom_data["nElements"]):
        fraction = atom_data["nAtoms"][i] / atom_data["nAtomsAll"]
        z = atom_data["Elements"][i]
        # Iterate over momentum transfer
        for j in range(len(sum_fs)):
            f = xraylib.FF_Rayl(z, q_xraylib[j])
            sum_squared_fs[j] += fraction * np.square(f)
            sum_fs[j] += fraction * f
    if mode == FORMFACTORKEYS.SUMOFSQUARES:
        result = sum_squared_fs
    elif mode == FORMFACTORKEYS.SQUAREOFSUMS:
        result = sum_fs * sum_fs
    else:
        raise VaxadiumConfigurationError(f"Unrecognised normalisation mode: {mode}")

    return result
