import math

import numpy as np
import xraylib

from vaxadium.constants import PHYSICAL


def g0_minus_one(material):
    atom_data = xraylib.CompoundParser(material)
    numerator = 0.0
    denominator = 0.0
    for i in range(atom_data["nElements"]):
        stoich = atom_data["nAtoms"][i]
        z = atom_data["Elements"][i]
        increment = stoich * z
        numerator += increment
        denominator += increment**2

    val = numerator**2 / denominator
    return val


def atom_number_density(formula, mass_density):
    data = xraylib.CompoundParser(formula)
    total_atoms = np.sum(data["nAtoms"])
    mol_per_cm3 = mass_density / data["molarMass"]
    mol_per_m3 = mol_per_cm3 * 1e6
    atoms_per_m3 = PHYSICAL.AVAGADRO.magnitude * mol_per_m3 * total_atoms
    return atoms_per_m3


def krogh_moe_sum(number_density, element_fraction_list, delta=0.0):
    summation = 0.0
    total_atoms = 0
    for zi, ci in element_fraction_list:
        total_atoms += ci

    for zi, ci in element_fraction_list:
        for zj, cj in element_fraction_list:
            summation += (
                (2 - kronecker_delta(zi, zj))
                * ci
                * cj
                * (-zi * zj + delta)
                / total_atoms**2
            )
            if zi == zj:
                break

    km = 2 * math.pi * math.pi * number_density * summation / 1e30
    return km


def krogh_moe_sum_from_formula(mass_density, formula):
    atom_data = xraylib.CompoundParser(formula)
    number_density = atom_number_density(formula, mass_density)

    atom_dict = []

    for i in range(len(atom_data["nAtoms"])):
        atom_dict.append(
            (atom_data["Elements"][i], atom_data["nAtoms"][i] / atom_data["nAtomsAll"])
        )

    return krogh_moe_sum(number_density, atom_dict)


def kronecker_delta(i, j):
    return 1 if (i == j) else 0


def thomson_dscs(tth, chi):
    sin_theta = np.sin(tth)
    cos_chi = np.cos(chi)
    return 1 - sin_theta * sin_theta * cos_chi * cos_chi
