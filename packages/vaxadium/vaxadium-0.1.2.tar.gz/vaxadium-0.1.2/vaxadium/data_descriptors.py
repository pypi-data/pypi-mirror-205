import logging

import numpy as np
import xraylib

from vaxadium.constants import DATAKEYS as DKEYS
from vaxadium.g4diffsim.fitting import Extraction

logger = logging.getLogger(__name__)


class LABELS:
    RAW = "raw"
    PREPROCESSED = "preprocessed"


class Component:
    """
    A component object describes a part of the sample. so a powder in
    a capillary is two components, the powder, and the capillary.

    the canonical "SAMPLE" is just the Component the user is interested in
    Every component has EXACTLY one:
        * attenuator object for doing absorption

    we use this wrapper instead of the attenuator directly for extensibility purposes
    """

    def __init__(self, attenuator):
        self.attenuator = attenuator


class DataHolder:
    def __init__(self, data=None, name=""):
        self.set_raw_data(data)
        self.name = name

    @property
    def data(self):
        return self._data[self._current_data_label]

    def set_raw_data(self, data):
        self._data = {}
        self.set_new_data(data, DKEYS.RAW)

    def reset_data(self):
        self._data = {DKEYS.RAW: self._data[DKEYS.RAW]}
        self._current_data_label = DKEYS.RAW

    def set_new_data(self, data, label):
        if label in self._data.keys():
            logger.debug(
                "Overwriting data with label {} in {}".format(label, self.name)
            )
        self._data[label] = data
        self._current_data_label = label

    def apply(self, function, new_label=None):
        new_label = new_label or function.__name__
        if new_label in self._data.keys():
            logger.debug(
                "Data label {} already exists in {}, aborting this apply call".format(
                    new_label, self.name
                )
            )
            return
        new_data = function(self.data)
        self.set_new_data(new_data, new_label)


class DataCollection(DataHolder):
    """
    A datacollection is essentially a thin API object which either comes from a nxs
    file or is manually constructed by the user. A data_collection has EXACTLY one:
        * dataset
        * pyFAI
        * transmission map detector
        * beam
    """

    def __init__(self, data=None, pyfai=None, detector=None, beam=None, name=None):
        super().__init__(data, name)
        self.pyfai = pyfai
        self.detector = detector
        self.beam = beam
        self.preprocessed = None
        self.name = name

    @property
    def solid_angle(self):
        return self.pyfai.solidAngleArray(absolute=True)

    @property
    def chi(self):
        return self.pyfai.chiArray()

    @property
    def tth(self):
        return self.pyfai.twoThetaArray()

    @property
    def r(self):
        return self.pyfai.rArray()

    @property
    def tth_chi_r(self):
        return (self.tth, self.chi, self.r)

    @property
    def detector_transmission(self):
        return self.calc_detector_transmission_correction().squeeze()

    def calc_detector_transmission_correction(self, energy=None, detector=None):
        if energy is None:
            energy = [self.beam.energy]
        detector = detector or self.detector
        # this method is a placeholder replacement for
        # Detector.transmission_from_origin(76.69)
        # which is sloooooooooooow #TODO tidy this up!
        (d1, d2) = (np.arange(d) for d in detector.n_pixels)
        x, y = np.meshgrid(d1, d2)
        try:
            mu = (
                np.array(
                    [xraylib.CS_Photo_CP(detector.material, e) / 10 for e in energy]
                )
                * detector.density
            )
        except AttributeError as e:
            logger.error("likely that no sensor properties set on detector" + str(e))
            raise
        result = np.exp(
            -mu[..., None, None]
            * detector.thickness
            / self.pyfai.cos_incidence(y, x)[None, ...]
        )
        return result

    def _already_preprocessed(self, label):
        if (
            self._current_data_label == LABELS.PREPROCESSED
            and not label == LABELS.PREPROCESSED
        ):
            logger.debug(
                "you are trying to preprocess already preprocessed "
                "data. The call to preprocess has been ignored. Override "
                "this behaviour by explicitly including preprocessed label "
            )
            already_preprocessed = True
        else:
            already_preprocessed = False
        return already_preprocessed

    def preprocess(self, label=None):
        if not self._already_preprocessed(label):
            label = label or self._current_data_label
            self._data[LABELS.PREPROCESSED] = (
                self._data[label] / self.beam.normalisation / self.solid_angle
            )
            self._current_data_label = LABELS.PREPROCESSED


class Simulation(DataCollection):
    """
    The simulation needs to be able to do everything the satacollection can do
    but also needs to manage the extraction process

    A wrapper class for a geant4 simulation. Not the same as the nexus reader
    which exclusievly reads the file and parses the info.
    this is a higher level wrapper which acts as an inteface to the g4 reader,
    but also handles the creation of a simulation which is not available.
    also does the preprocees maths, the attenutaion correction, the interpolation, etc
    A simulation has n components (ie g4 components) in it.
    hmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm

    """

    def __init__(
        self,
        data=None,
        pyfai=None,
        detector=None,
        beam=None,
        detector_energies=None,
        number_of_photons=0,
        name=None,
    ):
        super().__init__(data, pyfai, detector, beam, name)
        self.detector_energies = detector_energies
        self.number_of_photons = number_of_photons
        self.extraction = None

    def __eq__(self, other):
        """
        two simulations are equal if they have the same data,
        number_of_photons, detector_energies, beam, detector, and pyfai.
        """
        if type(other) is type(self):
            data = np.array_equal(self.data, other.data)
            n_photons = self.number_of_photons == other.number_of_photons
            det_energy = all(self.detector_energies == other.detector_energies)
            beam = self.beam == other.beam
            pyfai = str(self.pyfai) == str(other.pyfai)
            bools = (data, n_photons, det_energy, beam, pyfai)
            logger.debug("comparison of {} and {} --> {}".format(self, other, bools))
            return all(bools)
        else:
            return False

    @property
    def detector_transmission(self):
        return self.calc_detector_transmission_correction(self.detector_energies)

    def preprocess(self, label=None):
        if not self._already_preprocessed(label):
            logger.info("Starting preprocessing of {}...".format(self.name))
            label = label or self._current_data_label
            self._data[LABELS.PREPROCESSED] = (
                self._data[label]
                * (1 - self.detector_transmission)
                / self.solid_angle
                / self.number_of_photons
            ).sum(0)
            self._current_data_label = LABELS.PREPROCESSED
            logger.debug("simulation preprocessed")

    def fit(self, function, p0):
        """Creates an extraction object"""
        logger.info("performing fit extraction")
        self.extraction = Extraction.from_library()


class Background:
    def __init__(self, data=None):
        self.data = data
