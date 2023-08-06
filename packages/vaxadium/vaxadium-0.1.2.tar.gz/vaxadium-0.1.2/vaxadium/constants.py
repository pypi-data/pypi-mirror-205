"""Various constants used across the package.
Constants are loosely defined as anything which is required in more than one
place. In this file, they are organised into "Physical" and "Implementation".

Physical constants are usually numbers that represent a physical thing.

Implementation constants are things like group paths within nexus files, as
defined by the relevant nexus file definitions.
"""
from dataclasses import dataclass

from vaxadium.core.units import Q_, QA_


# Physical Constants
class PHYSICAL:
    ELECTRON_RADIUS = Q_(2.8179403227e-15, "m")
    SPEED_OF_LIGHT = Q_(299792458, "m / s")
    PLANCK_CONSTANT = Q_(6.62607004e-34, "m**2 kg / s")
    AVAGADRO = Q_(6.02214076e23)


class KEYS:
    DATA = "data"
    BEAM = "beam"
    PRIMARY_BEAM_ENERGY = "primary_beam_energy"
    PRIMARY_BEAM_WAVELENGTH = "primary_beam_wavelength"
    PRIMARY_BEAM_DIRECTION = "primary_beam_direction"
    PRIMARY_BEAM_ELLIPTICAL = "primary_beam_elliptical"
    PRIMARY_BEAM_HALF_X = "primary_beam_halfx"
    PRIMARY_BEAM_HALF_Y = "primary_beam_halfy"
    PRIMARY_BEAM_HALF_DIMENSIONS = "primary_beam_half_dimensions"
    PRIMARY_PHOTONS = "primary_photons"
    PRIMARY_BEAM_EXTENT = "primary_beam_extent"
    DETECTOR_HALF_X = "detector_half_x"
    DETECTOR_HALF_Y = "detector_half_y"
    DETECTOR_DISTANCE = "detector_distance"
    DETECTOR_ENERGY_BINS = "detector_energy_bins"
    DETECTOR_ORIGIN = "detector_origin"
    DETECTOR_THICKNESS = "detector_thickness"
    DETECTOR_MATERIAL = "detector_material"
    DETECTOR_DENSITY = "detector_density"
    DETECTOR_UI = "detector_ui"
    DETECTOR_UK = "detector_uk"
    DETECTOR_PONI1 = "detector_poni1"
    DETECTOR_PONI2 = "detector_poni2"
    DETECTOR_ROT1 = "detector_rot1"
    DETECTOR_ROT2 = "detector_rot2"
    DETECTOR_ROT3 = "detector_rot3"
    DETECTOR_PONI_FILEPATH = "detector_poni_filepath"
    DETECTOR_PYFAI_DIST = "detector_pyfai_dist"
    PIXEL_NUMBERS = "pixel_numbers"
    PIXEL_SIZES = "pixel_sizes"
    PIXEL_SIZE_FAST = "pixel_size_fast"
    PIXEL_SIZE_SLOW = "pixel_size_slow"
    SAMPLE_NUMBER = "number_of_samples"
    SAMPLEn_ATOMS = "sample{}_atoms"
    SAMPLEn_CHEMICAL_FORMULA = "sample{}_formula"
    SAMPLEn_DENSITY = "sample{}_density"
    SAMPLEn_HALF_DIMENSIONS = "sample{}_half_dimensions"
    SAMPLEn_DIMENSIONS = "sample{}_dimensions"
    SAMPLEn_MASS_FRACTIONS = "sample{}_mass_fractions"
    SAMPLEn_MATERIAL_NAME = "sample{}_material_name"
    SAMPLEn_NAME = "sample{}_name"
    SAMPLEn_RINNER = "sample{}_rinner"
    SAMPLEn_ROUTER = "sample{}_router"
    SAMPLEn_DESCRIPTION = "sample{}_description"
    SAMPLEn_VOLUME_FRACTION = "sample{}_volume_fraction"
    SAMPLEn_FILEPATH = "sample{}_filepath"
    BACKGROUND_FILEPATH = "background_filepath"
    BACKGROUND_DATA = "background_data"
    SAMPLEn_DATA = "sample{}_data"
    SIMULATIONn_FILEPATH = "simulation{}_filepath"
    SOURCE_FILE = "source_file_path"
    AXES_NAMES = "axes_names"
    AXES_VALUES = "axes_values"
    ATTENUATOR_TRANSMISSION = "attenuator_transmission"


class OLDJ15NXS:
    PRIMARY_BEAM_ENERGY = "/entry/sample/beam/incident_energy"
    PRIMARY_BEAM_EXTENT = "/entry/sample/beam/extent"
    DATA = "/entry/pe2AD/data"
    DETECTOR_DISTANCE = "/entry/instrument/pe2AD/distance"
    PIXEL_SIZE_FAST = "/entry/instrument/pe2AD/detector_module/fast_pixel_direction"
    PIXEL_SIZE_SLOW = "/entry/instrument/pe2AD/detector_module/slow_pixel_direction"
    DETECTOR_THICKNESS = "/entry/instrument/pe2AD/sensor_thickness"
    DETECTOR_MATERIAL = "/entry/instrument/pe2AD/sensor_material"
    DETECTOR_DENSITY = "/entry/instrument/pe2AD/sensor_density"
    DETECTOR_PONI_FILEPATH = "/entry/instrument/pe2AD/poni_file_path"
    CONTAINERS = "/entry/sample/containers"
    BACKGROUND_FILEPATH = "/entry/sample/containers/container_0/file_name"
    CONTAINERn_FILEPATH = "/entry/sample/containers/container_{}/file_name"
    SAMPLE_CHEMICAL_FORMULA = "/entry/sample/chemical_formula"
    SAMPLE_DENSITY = "/entry/sample/density"
    SAMPLE_DESCRIPTION = "/entry/sample/description"
    SAMPLE_NAME = "/entry/sample/name"
    SAMPLE_VOLUME_FRACTION = "/entry/sample/volume_fraction"
    SAMPLE_DIMENSIONS = "/entry/sample/shape/size"
    CONTAINERn_CHEMICAL_FORMULA = (
        "/entry/sample/containers/container_{}/chemical_formula"
    )
    CONTAINERn_DENSITY = "/entry/sample/containers/container_{}/density"
    CONTAINERn_DESCRIPTION = "/entry/sample/containers/container_{}/description"
    CONTAINERn_NAME = "/entry/sample/containers/container_{}/name"
    CONTAINERn_VOLUME_FRACTION = (
        "/entry/sample/containers/container_{}/packing_fraction"
    )
    CONTAINERn_DIMENSIONS = "/entry/sample/containers/container_{}/shape/size"
    PIXEL_NUMBERS = "/entry/instrument/pe2AD/detector_module/data_size"
    BACKGROUND_DATA = (
        "/entry/sample/containers/container_0/reference_measurement/pe2AD/data"
    )
    SAMPLEn_DATA = (
        "/entry/sample/containers/container_{}/reference_measurement/pe2AD/data"
    )
    UNIQUE_KEYS = "/entry/solstice_scan/keys/uniqueKeys"
    PIXEL_NUMBERS = "/entry/instrument/pe2AD/detector_module/data_size"
    DETECTOR_FOR_AXES = "/entry/pe2AD"
    ATTENUATOR_TRANSMISSION = (
        "/entry/instrument/experimental_hutch/f2/attenuator_transmission"
    )


class OLDG4NXS:
    PRIMARY_BEAM_ENERGY = "/entry/diffraction/instrument/energy"
    DETECTOR_DISTANCE = "/entry/diffraction/instrument/distance"
    PRIMARY_BEAM_HALF_X = "/entry/diffraction/instrument/beam_half_x"
    PRIMARY_BEAM_HALF_Y = "/entry/diffraction/instrument/beam_half_y"
    PRIMARY_PHOTONS = "/entry/diffraction/instrument/number_of_photons"
    DETECTOR_HALF_X = "/entry/diffraction/instrument/detector_half_x"
    DETECTOR_HALF_Y = "/entry/diffraction/instrument/detector_half_y"
    DETECTOR_ENERGY_BINS = "/entry/diffraction/data/energy"
    DATA = "/entry/diffraction/data/data"
    SAMPLES = "/entry/diffraction/sample"
    SAMPLEn_ATOMS = "/entry/diffraction/sample/sample_{}/atoms"
    SAMPLEn_DENSITY = "/entry/diffraction/sample/sample_{}/density"
    SAMPLEn_DIMENSIONS = "/entry/diffraction/sample/sample_{}/dimensions"
    SAMPLEn_MASS_FRACTIONS = "/entry/diffraction/sample/sample_{}/mass_fractions"
    SAMPLEn_MATERIAL_NAME = "/entry/diffraction/sample/sample_{}/material_name"
    SAMPLEn_NAME = "/entry/diffraction/sample/sample_{}/name"


class DATAKEYS:
    RAW = "raw"
    NORMIO = "normalised_to_io"
    SOLID_ANGLE = "solid_angle_corrected"
    SUBBAK = "background_subtracted"
    SUBCAP = "capillary_subtracted"
    SUBSIM = "simulation_subtracted"


@dataclass
class NexKey:
    address: str
    default_unit: str = None
    bothered: bool = True
    name: str = ""

    @property
    def unit_required(self):
        return bool(self.default_unit)

    def _set_name(self, name):
        self.name = name


class NexusKeyGroup:
    @classmethod
    def get_keys(cls):
        [
            v._set_name(k.lower())
            for k, v in vars(cls).items()
            if not k.startswith("_") and isinstance(v, NexKey)
        ]
        return {
            k.lower(): v
            for k, v in vars(cls).items()
            if not k.startswith("_") and isinstance(v, NexKey)
        }

    @classmethod
    def get_lambdas(cls):
        return {
            k.lower(): v
            for k, v in vars(cls).items()
            if not k.startswith("_") and callable(v)
        }


class NEWNEXUSKEYS(NexusKeyGroup):
    PRIMARY_BEAM_ENERGY = NexKey("/entry/sample/beam/incident_energy")
    PRIMARY_BEAM_EXTENT = NexKey("/entry/sample/beam/extent")
    CONTAINER0_CHEMICAL_FORMULA = NexKey(
        "/entry/sample/containers/container_0/chemical_formula"
    )


class NEWG4NEXUSKEYS(NexusKeyGroup):
    PRIMARY_BEAM_ENERGY = NexKey("/entry/diffraction/instrument/energy", "MeV")
    DETECTOR_DISTANCE = NexKey("/entry/diffraction/instrument/distance", "mm")
    PRIMARY_BEAM_HALF_X = NexKey("/entry/diffraction/instrument/beam_half_x", "um")
    PRIMARY_BEAM_HALF_Y = NexKey("/entry/diffraction/instrument/beam_half_y", "um")
    PRIMARY_PHOTONS = NexKey("/entry/diffraction/instrument/number_of_photons")
    DETECTOR_HALF_X = NexKey("/entry/diffraction/instrument/detector_half_x", "m")
    DETECTOR_HALF_Y = NexKey("/entry/diffraction/instrument/detector_half_y", "m")
    DETECTOR_ENERGY_BINS = NexKey("/entry/diffraction/data/energy", "keV")
    DATA = NexKey("/entry/diffraction/data/data")

    SAMPLE0_ATOMS = NexKey("/entry/diffraction/sample/sample_0/atoms")
    SAMPLE0_DENSITY = NexKey("/entry/diffraction/sample/sample_0/density", "g / cm³")
    SAMPLE0_DIMENSIONS = NexKey("/entry/diffraction/sample/sample_0/dimensions", "mm")
    SAMPLE0_MASS_FRACTIONS = NexKey("/entry/diffraction/sample/sample_0/mass_fractions")
    SAMPLE0_MATERIAL_NAME = NexKey("/entry/diffraction/sample/sample_0/material_name")
    SAMPLE0_NAME = NexKey("/entry/diffraction/sample/sample_0/name")

    SAMPLE1_ATOMS = NexKey("/entry/diffraction/sample/sample_1/atoms", None, False)
    SAMPLE1_DENSITY = NexKey(
        "/entry/diffraction/sample/sample_1/density", "g / cm³", False
    )
    SAMPLE1_DIMENSIONS = NexKey(
        "/entry/diffraction/sample/sample_1/dimensions", "mm", False
    )
    SAMPLE1_MASS_FRACTIONS = NexKey(
        "/entry/diffraction/sample/sample_1/mass_fractions", None, False
    )
    SAMPLE1_MATERIAL_NAME = NexKey(
        "/entry/diffraction/sample/sample_1/material_name", None, False
    )
    SAMPLE1_NAME = NexKey("/entry/diffraction/sample/sample_1/name", None, False)

    SAMPLE2_ATOMS = NexKey("/entry/diffraction/sample/sample_2/atoms", None, False)
    SAMPLE2_DENSITY = NexKey(
        "/entry/diffraction/sample/sample_2/density", "g / cm³", False
    )
    SAMPLE2_DIMENSIONS = NexKey(
        "/entry/diffraction/sample/sample_2/dimensions", "mm", False
    )
    SAMPLE2_MASS_FRACTIONS = NexKey(
        "/entry/diffraction/sample/sample_2/mass_fractions", None, False
    )
    SAMPLE2_MATERIAL_NAME = NexKey(
        "/entry/diffraction/sample/sample_2/material_name", None, False
    )
    SAMPLE2_NAME = NexKey("/entry/diffraction/sample/sample_2/name", None, False)

    PRIMARY_BEAM_WAVELENGTH = (
        lambda x: PHYSICAL.SPEED_OF_LIGHT
        * PHYSICAL.PLANCK_CONSTANT
        / x["primary_beam_energy"]
    )
    PRIMARY_BEAM_DIRECTION = lambda x: [0, 0, 1]
    PRIMARY_BEAM_ELLIPTICAL = lambda x: False
    NUMBER_OF_SAMPLES = lambda x: len([k for k in x.keys() if "mass_fractions" in k])
    PRIMARY_BEAM_HALF_DIMENSIONS = lambda x: (
        x["primary_beam_half_x"],
        x["primary_beam_half_y"],
    )
    PRIMARY_BEAM_HALF_DIMENSIONS = lambda x: QA_(
        [x["primary_beam_half_x"], x["primary_beam_half_y"]], "mm"
    )
    PIXEL_SIZES = lambda x: (
        2 * x["detector_half_x"] / x["data"].shape[2],
        2 * x["detector_half_y"] / x["data"].shape[1],
    )
    PIXEL_NUMBERS = lambda x: x["data"].shape[1:]


class NEWNXXPDFNEXUSKEYS(NexusKeyGroup):
    PRIMARY_BEAM_ENERGY = NexKey("/entry/sample/beam/incident_energy", "keV")
    PRIMARY_BEAM_EXTENT = NexKey("/entry/sample/beam/extent", "um")
    DETECTOR_DISTANCE = NexKey("/entry/instrument/pe2AD/distance", "mm")
    PIXEL_SIZE_FAST = NexKey(
        "/entry/instrument/pe2AD/detector_module/fast_pixel_direction", "mm"
    )
    PIXEL_SIZE_SLOW = NexKey(
        "/entry/instrument/pe2AD/detector_module/slow_pixel_direction", "mm"
    )
    PIXEL_NUMBERS = NexKey("/entry/instrument/pe2AD/detector_module/data_size")
    DETECTOR_THICKNESS = NexKey("/entry/instrument/pe2AD/sensor_thickness", "mm")
    DETECTOR_MATERIAL = NexKey("/entry/instrument/pe2AD/sensor_material")
    DETECTOR_DENSITY = NexKey("/entry/instrument/pe2AD/sensor_density", "g / cm³")
    DETECTOR_PONI_FILEPATH = NexKey("/entry/instrument/pe2AD/poni_file_path")

    BACKGROUND_FILEPATH = NexKey("/entry/sample/containers/container_0/file_name")
    BACKGROUND_DATA = NexKey(
        "/entry/sample/containers/container_0/reference_measurement/pe2AD/data"
    )

    SAMPLE0_FORMULA = NexKey("/entry/sample/chemical_formula")
    SAMPLE0_DENSITY = NexKey("/entry/sample/density", "g / cm³")
    SAMPLE0_DESCRIPTION = NexKey("/entry/sample/description")
    SAMPLE0_NAME = NexKey("/entry/sample/name")
    SAMPLE0_VOLUME_FRACTION = NexKey("/entry/sample/volume_fraction")
    SAMPLE0_DIMENSIONS = NexKey("/entry/sample/shape/size", "mm")

    SAMPLE1_FORMULA = NexKey(
        "/entry/sample/containers/container_1/chemical_formula", None, False
    )
    SAMPLE1_DENSITY = NexKey("/entry/sample/containers/container_1/density", "g / cm³")
    SAMPLE1_DESCRIPTION = NexKey("/entry/sample/containers/container_1/description")
    SAMPLE1_NAME = NexKey("/entry/sample/containers/container_1/name")
    SAMPLE1_VOLUME_FRACTION = NexKey(
        "/entry/sample/containers/container_1/packing_fraction"
    )
    SAMPLE1_DIMENSIONS = NexKey("/entry/sample/containers/container_1/shape/size", "mm")
    SAMPLE1_FILEPATH = NexKey("/entry/sample/containers/container_1/file_name")
    SAMPLE1_DATA = NexKey(
        "/entry/sample/containers/container_1/reference_measurement/pe2AD/data",
    )

    SAMPLE2_FORMULA = NexKey(
        "/entry/sample/containers/container_2/chemical_formula", None, False
    )
    SAMPLE2_DENSITY = NexKey("/entry/sample/containers/container_2/density", "g / cm³")
    SAMPLE2_DESCRIPTION = NexKey("/entry/sample/containers/container_2/description")
    SAMPLE2_NAME = NexKey("/entry/sample/containers/container_2/name")
    SAMPLE2_VOLUME_FRACTION = NexKey(
        "/entry/sample/containers/container_2/packing_fraction"
    )
    SAMPLE2_DIMENSIONS = NexKey("/entry/sample/containers/container_2/shape/size", "mm")
    SAMPLE2_FILEPATH = NexKey("/entry/sample/containers/container_2/file_name")
    SAMPLE2_DATA = NexKey(
        "/entry/sample/containers/container_2/reference_measurement/pe2AD/data",
    )

    UNIQUE_KEYS = NexKey("/entry/diamond_scan/keys/uniqueKeys")
    ATTENUATOR_TRANSMISSION = NexKey(
        "/entry/instrument/experimental_hutch/f2/attenuator_transmission"
    )

    _DETECTOR_FOR_AXES = "/entry/pe2AD"
    _DATA = "/entry/pe2AD/data/"

    # remember lambdas resolve before additional functions so anything pyfai
    # related cannot have a lambda
    PRIMARY_BEAM_HALF_DIMENSIONS = lambda x: x["primary_beam_extent"] / 2
    PIXEL_SIZES = lambda x: (x["pixel_size_slow"], x["pixel_size_fast"])
    NUMBER_OF_SAMPLES = lambda x: len([k for k in x.keys() if "formula" in k])
    PRIMARY_BEAM_WAVELENGTH = (
        lambda x: PHYSICAL.SPEED_OF_LIGHT
        * PHYSICAL.PLANCK_CONSTANT
        / x["primary_beam_energy"]
    )
    PRIMARY_BEAM_DIRECTION = lambda x: [0, 0, 1]
    PRIMARY_BEAM_ELLIPTICAL = lambda x: False

    N_POINTS = lambda x: len(x["unique_keys"]) if type(x) is list else 1


class NEWNXXPDFNEXUSKEYSARC(NexusKeyGroup):
    # note if you inherit from one of the other classes ytou don't get those
    # class varibales using vars()
    PRIMARY_BEAM_ENERGY = NexKey("/entry/sample/beam/incident_energy", "keV")
    PRIMARY_BEAM_EXTENT = NexKey("/entry/sample/beam/extent", "um")
    DETECTOR_DISTANCE = NexKey("/entry/instrument/arc1AD/distance", "mm")
    PIXEL_SIZE_FAST = NexKey(
        "/entry/instrument/arc1AD/detector_module/fast_pixel_direction", "mm"
    )
    PIXEL_SIZE_SLOW = NexKey(
        "/entry/instrument/arc1AD/detector_module/slow_pixel_direction", "mm"
    )
    PIXEL_NUMBERS = NexKey("/entry/instrument/arc1AD/detector_module/data_size")
    DETECTOR_THICKNESS = NexKey("/entry/instrument/arc1AD/sensor_thickness", "mm")
    DETECTOR_MATERIAL = NexKey("/entry/instrument/arc1AD/sensor_material")
    DETECTOR_DENSITY = NexKey("/entry/instrument/arc1AD/sensor_density", "g / cm³")
    DETECTOR_PONI_FILEPATH = NexKey("/entry/instrument/arc1AD/poni_file_path")

    BACKGROUND_FILEPATH = NexKey("/entry/sample/containers/container_0/file_name")
    BACKGROUND_DATA = NexKey(
        "/entry/sample/containers/container_0/reference_measurement/arc1AD/data"
    )

    SAMPLE0_FORMULA = NexKey("/entry/sample/chemical_formula")
    SAMPLE0_DENSITY = NexKey("/entry/sample/density", "g / cm³")
    SAMPLE0_DESCRIPTION = NexKey("/entry/sample/description")
    SAMPLE0_NAME = NexKey("/entry/sample/name")
    SAMPLE0_VOLUME_FRACTION = NexKey("/entry/sample/volume_fraction")
    SAMPLE0_DIMENSIONS = NexKey("/entry/sample/shape/size", "mm")

    SAMPLE1_FORMULA = NexKey(
        "/entry/sample/containers/container_1/chemical_formula", None, False
    )
    SAMPLE1_DENSITY = NexKey("/entry/sample/containers/container_1/density", "g / cm³")
    SAMPLE1_DESCRIPTION = NexKey("/entry/sample/containers/container_1/description")
    SAMPLE1_NAME = NexKey("/entry/sample/containers/container_1/name")
    SAMPLE1_VOLUME_FRACTION = NexKey(
        "/entry/sample/containers/container_1/packing_fraction"
    )
    SAMPLE1_DIMENSIONS = NexKey("/entry/sample/containers/container_1/shape/size", "mm")
    SAMPLE1_FILEPATH = NexKey("/entry/sample/containers/container_1/file_name")
    SAMPLE1_DATA = NexKey(
        "/entry/sample/containers/container_1/reference_measurement/arc1AD/data",
    )

    SAMPLE2_FORMULA = NexKey(
        "/entry/sample/containers/container_2/chemical_formula", None, False
    )
    SAMPLE2_DENSITY = NexKey("/entry/sample/containers/container_2/density", "g / cm³")
    SAMPLE2_DESCRIPTION = NexKey("/entry/sample/containers/container_2/description")
    SAMPLE2_NAME = NexKey("/entry/sample/containers/container_2/name")
    SAMPLE2_VOLUME_FRACTION = NexKey(
        "/entry/sample/containers/container_2/packing_fraction"
    )
    SAMPLE2_DIMENSIONS = NexKey("/entry/sample/containers/container_2/shape/size", "mm")
    SAMPLE2_FILEPATH = NexKey("/entry/sample/containers/container_2/file_name")
    SAMPLE2_DATA = NexKey(
        "/entry/sample/containers/container_2/reference_measurement/arc1AD/data",
    )

    UNIQUE_KEYS = NexKey("/entry/diamond_scan/keys/uniqueKeys")
    ATTENUATOR_TRANSMISSION = NexKey(
        "/entry/instrument/experimental_hutch/f2/attenuator_transmission"
    )

    _DETECTOR_FOR_AXES = "/entry/arc1AD"
    _DATA = "/entry/arc1AD/data/"

    # remember lambdas resolve before additional functions so anything pyfai
    # related cannot have a lambda
    PRIMARY_BEAM_HALF_DIMENSIONS = lambda x: x["primary_beam_extent"] / 2
    PIXEL_SIZES = lambda x: (x["pixel_size_slow"], x["pixel_size_fast"])
    NUMBER_OF_SAMPLES = lambda x: len([k for k in x.keys() if "formula" in k])
    PRIMARY_BEAM_WAVELENGTH = (
        lambda x: PHYSICAL.SPEED_OF_LIGHT
        * PHYSICAL.PLANCK_CONSTANT
        / x["primary_beam_energy"]
    )
    PRIMARY_BEAM_DIRECTION = lambda x: [0, 0, 1]
    PRIMARY_BEAM_ELLIPTICAL = lambda x: False

    N_POINTS = lambda x: len(x["unique_keys"]) if type(x) is list else 1


class NEWNXXPDFNEXUSKEYSBKG(NexusKeyGroup):
    DATA = NexKey("/entry/pe2AD/data")
    """
    PRIMARY_BEAM_ENERGY = NexKey("/entry/sample/beam/incident_energy", "keV")
    PRIMARY_BEAM_EXTENT = NexKey("/entry/sample/beam/extent", "um")
    DETECTOR_DISTANCE = NexKey("/entry/instrument/pe2AD/distance", "mm")
    PIXEL_SIZE_FAST = NexKey(
        "/entry/instrument/pe2AD/detector_module/fast_pixel_direction", "mm"
    )
    PIXEL_SIZE_SLOW = NexKey(
        "/entry/instrument/pe2AD/detector_module/slow_pixel_direction", "mm"
    )
    PIXEL_NUMBERS = NexKey("/entry/instrument/pe2AD/detector_module/data_size")
    DETECTOR_THICKNESS = NexKey("/entry/instrument/pe2AD/sensor_thickness", "mm")
    DETECTOR_MATERIAL = NexKey("/entry/instrument/pe2AD/sensor_material")
    DETECTOR_DENSITY = NexKey("/entry/instrument/pe2AD/sensor_density", "g / cm³")
    DETECTOR_PONI_FILEPATH = NexKey("/entry/instrument/pe2AD/poni_file_path")

    BACKGROUND_FILEPATH = NexKey("/entry/sample/containers/container_0/file_name")
    BACKGROUND_DATA = NexKey(
        "/entry/sample/containers/container_0/reference_measurement/pe2AD/data"
    )

    SAMPLE0_FORMULA = NexKey("/entry/sample/chemical_formula")
    SAMPLE0_DENSITY = NexKey("/entry/sample/density", "g / cm³")
    SAMPLE0_DESCRIPTION = NexKey("/entry/sample/description")
    SAMPLE0_NAME = NexKey("/entry/sample/name")
    SAMPLE0_VOLUME_FRACTION = NexKey("/entry/sample/volume_fraction")
    SAMPLE0_DIMENSIONS = NexKey("/entry/sample/shape/size", "mm")

    SAMPLE1_FORMULA = NexKey(
        "/entry/sample/containers/container_1/chemical_formula", None, False
    )
    SAMPLE1_DENSITY = NexKey("/entry/sample/containers/container_1/density", "g / cm³")
    SAMPLE1_DESCRIPTION = NexKey("/entry/sample/containers/container_1/description")
    SAMPLE1_NAME = NexKey("/entry/sample/containers/container_1/name")
    SAMPLE1_VOLUME_FRACTION = NexKey(
        "/entry/sample/containers/container_1/packing_fraction"
    )
    SAMPLE1_DIMENSIONS = NexKey("/entry/sample/containers/container_1/shape/size", "mm")
    SAMPLE1_FILEPATH = NexKey("/entry/sample/containers/container_1/file_name")
    SAMPLE1_DATA = NexKey(
        "/entry/sample/containers/container_1/reference_measurement/pe2AD/data",
    )

    SAMPLE2_FORMULA = NexKey(
        "/entry/sample/containers/container_2/chemical_formula", None, False
    )
    SAMPLE2_DENSITY = NexKey("/entry/sample/containers/container_2/density", "g / cm³")
    SAMPLE2_DESCRIPTION = NexKey("/entry/sample/containers/container_2/description")
    SAMPLE2_NAME = NexKey("/entry/sample/containers/container_2/name")
    SAMPLE2_VOLUME_FRACTION = NexKey(
        "/entry/sample/containers/container_2/packing_fraction"
    )
    SAMPLE2_DIMENSIONS = NexKey("/entry/sample/containers/container_2/shape/size", "mm")
    SAMPLE2_FILEPATH = NexKey("/entry/sample/containers/container_2/file_name")
    SAMPLE2_DATA = NexKey(
        "/entry/sample/containers/container_2/reference_measurement/pe2AD/data",
    )

    UNIQUE_KEYS = NexKey("/entry/diamond_scan/keys/uniqueKeys")
    ATTENUATOR_TRANSMISSION = NexKey(
        "/entry/instrument/experimental_hutch/f2/attenuator_transmission"
    )

    _DETECTOR_FOR_AXES = "/entry/pe2AD"
    _DATA = "/entry/pe2AD/data/"

    # remember lambdas resolve before additional functions so anything pyfai
    # related cannot have a lambda
    PRIMARY_BEAM_HALF_DIMENSIONS = lambda x: (x["primary_beam_extent"] / 2)
    PIXEL_SIZES = lambda x: (x["pixel_size_slow"], x["pixel_size_fast"])
    NUMBER_OF_SAMPLES = lambda x: len([k for k in x.keys() if "formula" in k])
    PRIMARY_BEAM_WAVELENGTH = (
        lambda x: PHYSICAL.SPEED_OF_LIGHT
        * PHYSICAL.PLANCK_CONSTANT
        / x["primary_beam_energy"]
    )
    PRIMARY_BEAM_DIRECTION = lambda x: [0, 0, 1]
    PRIMARY_BEAM_ELLIPTICAL = lambda x: False
    """


class NEWNXXPDFNEXUSKEYSBKGARC(NEWNXXPDFNEXUSKEYSARC):
    DATA = NexKey("/entry/pe2AD/data")
