import logging

from pyFAI.azimuthalIntegrator import AzimuthalIntegrator
from pyFAI.detectors import Detector as PDetector

from vaxadium import defaults
from vaxadium.axes import Axis
from vaxadium.constants import KEYS
from vaxadium.core.detector import Detector
from vaxadium.data_descriptors import DataCollection, Simulation
from vaxadium.g4diffsim.macros import (
    G4BeamMacro,
    G4DetectorMacro,
    G4MaterialsMacro,
    G4PhysicsMacro,
    G4SampleMacro,
    G4WorldMacro,
)
from vaxadium.scaler import ScaledResultsCollection
from vaxadium.transmission import Attenuator, Beam

logger = logging.getLogger(__name__)


class DummySerializer:
    def __init__(self):
        self._current_object = None

    def log_to(self, destination):
        logger.debug(
            "serializing {} from {}".format(
                destination, self._current_object[KEYS.SOURCE_FILE]
            )
        )

    def start_object(self, source):
        self._current_object = {"from": source}

    def add_property(self, name, value):
        self._current_object[name] = value

    def get(self):
        logger.info("serializing to dictionary")
        return self._current_object


class BeamSerializer(DummySerializer):
    def get(self):
        self.log_to("beam")
        params = {}
        params[KEYS.PRIMARY_BEAM_ENERGY] = (
            self._current_object[KEYS.PRIMARY_BEAM_ENERGY].to("keV").magnitude
        )  # keV
        params[KEYS.PRIMARY_BEAM_DIRECTION] = self._current_object[
            KEYS.PRIMARY_BEAM_DIRECTION
        ]
        params[KEYS.PRIMARY_BEAM_ELLIPTICAL] = self._current_object[
            KEYS.PRIMARY_BEAM_ELLIPTICAL
        ]
        params[KEYS.PRIMARY_BEAM_HALF_DIMENSIONS] = (
            self._current_object[KEYS.PRIMARY_BEAM_HALF_DIMENSIONS].to("mm").magnitude
        )
        if KEYS.ATTENUATOR_TRANSMISSION in self._current_object.keys():
            params[KEYS.ATTENUATOR_TRANSMISSION] = (
                self._current_object[KEYS.ATTENUATOR_TRANSMISSION] / 100
            )
        return Beam(params)


class DetectorSerializer(DummySerializer):
    def get(self):
        self.log_to("detector")
        params = {}
        params[KEYS.DETECTOR_DISTANCE] = (
            self._current_object[KEYS.DETECTOR_DISTANCE].to("mm").magnitude
        )  # mm
        params[KEYS.PIXEL_SIZES] = [
            x.to("mm").magnitude for x in self._current_object[KEYS.PIXEL_SIZES]
        ]
        params[KEYS.DETECTOR_ORIGIN] = (
            self._current_object[KEYS.DETECTOR_ORIGIN].to("mm").magnitude
        )  # mm
        params[KEYS.DETECTOR_UI] = self._current_object[KEYS.DETECTOR_UI]
        params[KEYS.DETECTOR_UK] = self._current_object[KEYS.DETECTOR_UK]
        params[KEYS.PIXEL_NUMBERS] = tuple(
            self._current_object[KEYS.PIXEL_NUMBERS]
        )  # TODO remove this tuple hack
        if KEYS.DETECTOR_THICKNESS in self._current_object.keys():
            params[KEYS.DETECTOR_THICKNESS] = (
                self._current_object[KEYS.DETECTOR_THICKNESS].to("mm").magnitude
            )  # mm
        if KEYS.DETECTOR_MATERIAL in self._current_object.keys():
            params[KEYS.DETECTOR_MATERIAL] = str(
                self._current_object[KEYS.DETECTOR_MATERIAL]
            )
        if KEYS.DETECTOR_DENSITY in self._current_object.keys():
            params[KEYS.DETECTOR_DENSITY] = (
                self._current_object[KEYS.DETECTOR_DENSITY].to("g/cm³").magnitude
            )
        return Detector(params)


class AttenuatorsSerializer(DummySerializer):
    def get(self):
        self.log_to("attenuators")
        params = {}
        for i in range(self._current_object[KEYS.SAMPLE_NUMBER]):
            dimensions = (
                self._current_object[KEYS.SAMPLEn_DIMENSIONS.format(i)]
                .to("cm")
                .magnitude
                / 2
            )
            params[KEYS.SAMPLEn_RINNER.format(i)] = dimensions[1]  # cm, radius
            params[KEYS.SAMPLEn_ROUTER.format(i)] = dimensions[0]  # cm, radius
            params[KEYS.SAMPLEn_CHEMICAL_FORMULA.format(i)] = self._current_object[
                KEYS.SAMPLEn_CHEMICAL_FORMULA.format(i)
            ]
            params[KEYS.SAMPLEn_DENSITY.format(i)] = (
                self._current_object[KEYS.SAMPLEn_DENSITY.format(i)]
                .to("g / cm ** 3")
                .magnitude
            )
            params[KEYS.SAMPLEn_VOLUME_FRACTION.format(i)] = self._current_object[
                KEYS.SAMPLEn_VOLUME_FRACTION.format(i)
            ]
        return [
            Attenuator(params, i)
            for i in range(self._current_object[KEYS.SAMPLE_NUMBER])
        ]


class Geant4MacrosSerializer(DummySerializer):
    def get(self):
        if self._current_object["from"] == "g4":
            logger.warning("should not serialize Experiment from g4.nxs")
        self.log_to("geant4 macro")
        world = G4WorldMacro()
        physics = G4PhysicsMacro()
        materials = G4MaterialsMacro()
        beam = G4BeamMacro()
        samples = G4SampleMacro()
        detector = G4DetectorMacro()
        if self._current_object[KEYS.SAMPLE_NUMBER] < 1:
            logger.error("serializable has no samples, macro files incomplete")
            raise NotImplementedError
        for i in range(self._current_object[KEYS.SAMPLE_NUMBER]):
            sample_name = self._current_object[KEYS.SAMPLEn_NAME.format(i)].replace(
                " ", "_"
            ) + "_{}".format(i)
            material_name = sample_name + "_material"
            materials.addMaterial(
                material_name,
                self._current_object[KEYS.SAMPLEn_ATOMS.format(i)],
                self._current_object[KEYS.SAMPLEn_DENSITY.format(i)]
                .to("g / cm ** 3")
                .magnitude
                * self._current_object[KEYS.SAMPLEn_VOLUME_FRACTION.format(i)],
                self._current_object[KEYS.SAMPLEn_MASS_FRACTIONS.format(i)],
            )
            # reverse the order from outer, inner, length to inner, outer, length
            # and diameters to radii
            wrong_dims = (
                self._current_object[KEYS.SAMPLEn_DIMENSIONS.format(i)]
                .to("mm")
                .magnitude.tolist()
            )
            dims = [wrong_dims[1] / 2, wrong_dims[0] / 2, wrong_dims[2]]
            samples.addSample(sample_name, dims, material_name)
        pb_energy = self._current_object[KEYS.PRIMARY_BEAM_ENERGY].to("keV").magnitude
        pb_half_x, pb_half_y = (
            self._current_object[KEYS.PRIMARY_BEAM_HALF_DIMENSIONS].to("mm").magnitude
        )
        beam.addBeam(
            2 * defaults.G4DIFFSIM.DET_EBINS,
            2 * pb_energy,
            pb_energy,
            pb_half_x,
            pb_half_y,
        )
        if self._current_object["detector_shape"] == "cylinder":
            detector.addDiffractionDetectorCylinder(
                defaults.G4DIFFSIM.ARC_RADIUS.to("cm").magnitude,
                defaults.G4DIFFSIM.ARC_TWOTHETA.to("degrees").magnitude,
                defaults.G4DIFFSIM.ARC_XPIXELS,
                defaults.G4DIFFSIM.ARC_YPIXELS,
                defaults.G4DIFFSIM.ARC_HALFWIDTH.to("mm").magnitude,
                defaults.G4DIFFSIM.DET_EBINS,
                defaults.G4DIFFSIM.DET_EMAX.to("keV").magnitude,
            )
        else:
            detector.addDiffractionDetectorFlat(
                defaults.G4DIFFSIM.DET_DIST.to("cm").magnitude,
                defaults.G4DIFFSIM.DET_XPIXELS,
                defaults.G4DIFFSIM.DET_YPIXELS,
                defaults.G4DIFFSIM.DET_SIZE.to("cm").magnitude.tolist(),
                defaults.G4DIFFSIM.DET_EBINS,
                defaults.G4DIFFSIM.DET_EMAX.to("keV").magnitude,
            )
        return [world, beam, physics, materials, samples, detector]


class SimulationSerializer(DummySerializer):
    def get(self):
        self.log_to("simulation")
        data = self._current_object[KEYS.DATA]
        pyfai = PyFAISerializer.get(self)
        detector = DetectorSerializer.get(self)
        beam = BeamSerializer.get(self)
        detector_energies = self._current_object[KEYS.DETECTOR_ENERGY_BINS].magnitude
        number_of_photons = self._current_object[KEYS.PRIMARY_PHOTONS]
        name = self._current_object[KEYS.SAMPLEn_NAME.format(0)]
        simulation = Simulation(
            data, pyfai, detector, beam, detector_energies, number_of_photons, name
        )
        return simulation


class DataCollectionsSerializer(DummySerializer):
    def get(self):
        self.log_to("data collection")
        data_collections = []
        for i in range(self._current_object[KEYS.SAMPLE_NUMBER]):
            logger.debug("serializing sample {}".format(i))
            data = None
            pyfai = PyFAISerializer.get(self)
            detector = DetectorSerializer.get(self)
            beam = BeamSerializer.get(self)
            data_collection = [DataCollection(data, pyfai, detector, beam)]
            data_collections += data_collection
        return data_collections


class BackgroundSerializer(DummySerializer):
    def get(self):
        self.log_to("background")

        data = self._current_object[KEYS.DATA]
        pyfai = PyFAISerializer.get(self)
        detector = DetectorSerializer.get(self)
        beam = BeamSerializer.get(self)
        data_collection = DataCollection(data, pyfai, detector, beam)
        data_collection.name = "background"
        return data_collection


class PyFAISerializer(DummySerializer):
    def get(self):
        self.log_to("pyfai")
        pixel_sizes = [
            x.to("m").magnitude for x in self._current_object[KEYS.PIXEL_SIZES]
        ]
        logger.debug("pixel sizes: {}".format(pixel_sizes))
        det_shape = list(self._current_object[KEYS.PIXEL_NUMBERS])
        pdet = PDetector(
            pixel1=pixel_sizes[0], pixel2=pixel_sizes[1], max_shape=det_shape
        )
        distance = self._current_object[KEYS.DETECTOR_PYFAI_DIST].to("m").magnitude
        wavelength = (
            self._current_object[KEYS.PRIMARY_BEAM_WAVELENGTH].to("m").magnitude
        )
        ai = AzimuthalIntegrator(dist=distance, wavelength=wavelength, detector=pdet)
        ai.set_poni1(self._current_object[KEYS.DETECTOR_PONI1].to("m").magnitude)
        ai.set_poni2(self._current_object[KEYS.DETECTOR_PONI2].to("m").magnitude)
        ai.set_rot1(self._current_object[KEYS.DETECTOR_ROT1].to("radians").magnitude)
        ai.set_rot2(self._current_object[KEYS.DETECTOR_ROT2].to("radians").magnitude)
        ai.set_rot3(self._current_object[KEYS.DETECTOR_ROT3].to("radians").magnitude)
        return ai


class ScaledExperimentCollectionSerializer(DummySerializer):
    def get(self):
        axes = []
        for name, values in zip(
            self._current_object[KEYS.AXES_NAMES],
            self._current_object[KEYS.AXES_VALUES],
        ):
            axes += [Axis(name, values)]
        return ScaledResultsCollection(axes)
