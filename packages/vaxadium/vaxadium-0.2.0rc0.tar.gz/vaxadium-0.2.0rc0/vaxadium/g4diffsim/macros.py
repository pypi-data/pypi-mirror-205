import logging
from collections import OrderedDict  # to make sure lines are added in the correct order
from numbers import Number  # for type checking

logger = logging.getLogger(__name__)


def convert_units(value_unit_pair, multiplier=1):
    original_value = value_unit_pair[0]
    original_unit = value_unit_pair[1]
    magnitudes = {"G": 9, "M": 6, "k": 3, "c": -2, "m": -3, "u": -6, "n": -9, "p": -12}
    return multiplier * original_value * 10.0 ** (magnitudes[original_unit[0]])


class G4Macro(object):
    def __init__(self, header=""):
        self.paths = {}
        self.lines = OrderedDict()
        divider = "#" + "-" * 59
        self.header = ["", divider, header, ""]

    def echo(self):
        # create the outputs
        if len(self.lines.keys()) == 0:
            logger.warning(
                'there are no lines in this G4Macro "{}".'.format(self.header[2])
            )
        return self.header + [
            line[0].format(**self.paths) + " ".join([" {}".format(v) for v in line[1]])
            for line in self.lines.values()
        ]


class G4PhysicsMacro(G4Macro):
    def __init__(self):
        super().__init__("# Controlling the physics")
        self.paths = {
            "livermore": "/physics/gamma/livermore",
            "gamma": "/physics/gamma",
        }
        self.lines["photoelectric"] = ["{livermore}/photoelectric", [True]]
        self.lines["compton"] = ["{livermore}/comptonscattering", [True]]
        self.lines["rayleigh"] = ["{livermore}/rayleighscattering", [True]]
        self.lines["fluorescence"] = ["{gamma}/fluorescence", [True]]
        self.lines["refraction"] = ["{gamma}/refraction", [False]]
        self.lines["cuts"] = ["{gamma}/cuts", [10, "um"]]


class G4MaterialsMacro(G4Macro):
    def __init__(self):
        super().__init__("# Defining the materials")
        self.paths = {
            "define": "/materials/define/compound",
            "addto": "/materials/addto/compound",
        }
        self.n_materials = 0

    def addMaterial(self, material_name, atoms, density, mass_fractions):
        assert isinstance(material_name, str), "material name must be a string"
        assert isinstance(atoms, list), "atoms must be a list"
        assert all(
            [isinstance(a, str) for a in atoms]
        ), "atoms must be a list of strings (specifically symbols)"
        assert isinstance(density, Number), "density should be a number"
        assert all(
            [isinstance(a, Number) for a in mass_fractions]
        ), "atoms must be a list of strings (specifically symbols)"
        assert len(mass_fractions) == len(
            atoms
        ), "mass fractions and atoms should be the same length"
        self.n_materials += 1
        i = self.n_materials
        number_of_atoms = len(atoms)
        self.lines["sample_{}_def".format(i)] = [
            "{define}",
            [material_name, number_of_atoms, density, "g/cm3"],
        ]
        for ia in range(number_of_atoms):
            self.lines["sample_{}_a{}".format(i, ia)] = [
                "{addto}",
                [material_name, atoms[ia], mass_fractions[ia] * 100, "%"],
            ]
        self.lines["sample_{}_blankline".format(i)] = ["", ""]

    def addMaterialsFromDict(self, samples):
        for sample in samples.values():
            self.addMaterial(
                sample["material_name"],
                sample["atoms"],
                sample["density"],
                sample["mass_fractions"],
            )


class G4SampleMacro(G4Macro):
    def __init__(self):
        super().__init__("# Defining the samples. Note these are radii.")
        self.colours = [
            "blue",
            "red",
        ] * 10  # not currently aware of what other colours are allowed
        self.paths = {
            "cylinder": "/sample/G4VSolid/cylinder",
            "logical": "/sample/G4LogicalVolume",
            "physical": "/sample/G4VPhysicalVolume",
        }
        self.n_samples = 0

    def addSample(self, name, dimensions, material_name):
        assert isinstance(name, str), "name must be a string"
        assert (
            isinstance(dimensions, list) and len(dimensions) == 3
        ), "dimensions must be a list of length 3"
        assert all(
            [isinstance(f, Number) for f in dimensions]
        ), "dimensions should all be numerics and the values should be in mm"
        self.n_samples += 1
        i = self.n_samples
        self.lines["sample_{}_sol".format(i)] = [
            "{cylinder}",
            [name, *dimensions, "mm 0. 360. deg"],
        ]
        self.lines["sample_{}_mat".format(i)] = [
            "{logical}/material",
            [name, material_name],
        ]
        self.lines["sample_{}_col".format(i)] = [
            "{logical}/colour",
            [name, self.colours[i]],
        ]
        self.lines["sample_{}_pos".format(i)] = [
            "{physical}/position",
            [name, "0.0 0.0 0.0 mm"],
        ]
        self.lines["sample_{}_rot".format(i)] = [
            "{physical}/rotation",
            [name, "0.0 90.0 0.0 deg"],
        ]
        self.lines["sample_{}_bla".format(i)] = ["", ""]

    def addSamplesFromDict(self, samples):
        for sample in samples.values():
            self.addSample(
                sample["name"], sample["dimensions"], sample["material_name"]
            )


class G4WorldMacro(G4Macro):
    def __init__(self):
        super().__init__("# Defining the World")
        self.paths = {"world": "/world"}
        self.lines["world_size"] = ["{world}/halfdimensions", [51.0, 51.0, 21.0, "cm"]]
        self.lines["world_material"] = ["{world}/material", ["G4_Galactic"]]  # G4_AIR


class G4DetectorMacro(G4Macro):
    def __init__(self):
        super().__init__("# Defining the Diffraction Detector")
        self.paths = {"diffraction": "/detector/diffraction"}

    def addDiffractionDetectorFlat(
        self,
        distance,
        pixel_number_x,
        pixel_number_y,
        detector_half_dimensions,
        n_energy_bins,
        max_energy,
    ):
        assert (
            isinstance(pixel_number_x, int) and pixel_number_x % 2 == 1
        ), "pixel_number_x should be an odd integer"
        assert (
            isinstance(pixel_number_y, int) and pixel_number_y % 2 == 1
        ), "pixel_number_y should be an odd integer"
        assert isinstance(
            detector_half_dimensions, list
        ), "half dimensions should be a list"
        assert (
            len(detector_half_dimensions) == 3
        ), "half dimensions should be a list of length 3"
        assert all(
            [isinstance(d, Number) for d in detector_half_dimensions]
        ), "hlaf dimensions should be a list of numbers"
        assert isinstance(n_energy_bins, int), "n_energy_bins should be int"
        assert isinstance(max_energy, Number), "max energy should be a number"
        self.lines["xpixels"] = ["{diffraction}/xpixels", [pixel_number_x]]
        self.lines["ypixels"] = ["{diffraction}/ypixels", [pixel_number_y]]
        self.lines["halfdimensions"] = [
            "{diffraction}/halfdimensions",
            [*detector_half_dimensions, "cm"],
        ]
        self.lines["bins"] = ["{diffraction}/bins", [n_energy_bins]]
        self.lines["max_energy"] = ["{diffraction}/maxenergy", [max_energy, "keV"]]
        self.lines["distance"] = ["{diffraction}/distance", [distance, "cm"]]
        self.lines["shape"] = ["{diffraction}/shape", ["flat"]]

    def addDiffractionDetectorCylinder(
        self,
        radius,
        twotheta,
        pixel_number_x,
        pixel_number_y,
        halfwidth,
        n_energy_bins,
        max_energy,
    ):
        assert (
            isinstance(pixel_number_x, int) and pixel_number_x % 2 == 1
        ), "pixel_number_x should be an odd integer"
        assert (
            isinstance(pixel_number_y, int) and pixel_number_y % 2 == 1
        ), "pixel_number_y should be an odd integer"
        assert isinstance(n_energy_bins, int), "n_energy_bins should be int"
        assert isinstance(max_energy, Number), "max energy should be a number"
        self.lines["xpixels"] = ["{diffraction}/xpixels", [pixel_number_x]]
        self.lines["ypixels"] = ["{diffraction}/ypixels", [pixel_number_y]]
        self.lines["shape"] = ["{diffraction}/shape", ["cylinder"]]
        self.lines["halfwidth"] = ["{diffraction}/halfwidth", [halfwidth, "mm"]]
        self.lines["bins"] = ["{diffraction}/bins", [n_energy_bins]]
        self.lines["max_energy"] = ["{diffraction}/maxenergy", [max_energy, "keV"]]
        self.lines["radius"] = ["{diffraction}/radius", [radius, "cm"]]
        self.lines["twotheta"] = ["{diffraction}/twotheta", [twotheta, "deg"]]

    def addDiffractionDetectorFromDict(self, metadata):
        pixel_number_x = metadata["pixel_number_x"]
        pixel_number_y = metadata["pixel_number_y"]
        bins = metadata["n_energies"]
        max_energy = metadata["energies_max"]
        shape = metadata.get("shape")
        if shape and shape == "cylinder":
            radius_cm = convert_units(metadata.get("radius"), 100)
            two_theta = metadata.get("two_theta")
            halfwidth = metadata.get("half")
            self.addDiffractionDetectorCylinder(
                radius_cm,
                two_theta,
                pixel_number_x,
                pixel_number_y,
                halfwidth,
                bins,
                max_energy,
            )

        if shape and shape == "flat":
            # Need to convert units in some cases
            distance_cm = convert_units(metadata["distance"], 100)
            detector_half_x = metadata["detector_half_x"]
            detector_half_y = metadata["detector_half_y"]
            detector_half_x_cm, detector_half_y_cm = map(
                lambda x: convert_units(x, 100), (detector_half_x, detector_half_y)
            )
            dimensions = [detector_half_x_cm, detector_half_y_cm, 0.01]
            self.addDiffractionDetectorFlat(
                distance_cm,
                pixel_number_x,
                pixel_number_y,
                dimensions,
                bins,
                max_energy,
            )


class G4BeamMacro(G4Macro):
    def __init__(self):
        super().__init__("# Defining the primary beam")
        self.paths = {"beam": "/beam"}

    def addBeam(self, bins, max_energy, primary_energy, half_x, half_y):
        self.lines["bins"] = ["{beam}/bins", [bins]]
        self.lines["max_energy"] = ["{beam}/maxenergy", [max_energy, "keV"]]
        self.lines["gps"] = ["{beam}/gps", ["false"]]
        self.lines["primary_energy"] = ["{beam}/energy/mono", [primary_energy, "keV"]]
        self.lines["momentum"] = ["{beam}/momentum", [0.0, 0.0, 1.0]]
        self.lines["auto"] = ["{beam}/pos/auto", ["false"]]
        self.lines["centre"] = ["{beam}/pos/centre", [0.0, 0.0, -10.0, "cm"]]
        self.lines["halfx"] = ["{beam}/pos/halfx", [half_x, "mm"]]
        self.lines["halfy"] = ["{beam}/pos/halfy", [half_y, "mm"]]
        self.lines["particle"] = ["{beam}/particle", ["gamma"]]

    def addBeamFromDict(self, metadata):
        bins = 2000
        max_energy = 175  # keV
        primary_energy = convert_units(metadata["energy"], 0.001)
        half_x = convert_units(metadata["beam_half_x"], 1000)
        half_y = convert_units(metadata["beam_half_y"], 1000)
        self.addBeam(bins, max_energy, primary_energy, half_x, half_y)
