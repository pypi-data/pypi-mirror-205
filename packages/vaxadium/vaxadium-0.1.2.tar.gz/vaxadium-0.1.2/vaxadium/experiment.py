import logging
import time
from copy import deepcopy

import numpy as np

from vaxadium.constants import PHYSICAL
from vaxadium.g4diffsim import fitting
from vaxadium.physics import atom_number_density
from vaxadium.transmission.transmission_map import TransmissionMap

logger = logging.getLogger(__name__)


class Experiment:
    """
    A thin, lightweight description of the experiment. either comes from a
    nexus file via a serializefr factory, or made manually

    is it anything more than just a tuple of components?
    yes! it has the background in there. and possibly some other things....?
    well. what links the experiment? The componennts. And what do the components give?
    the transmission maps.


    TO BE EXPLICIT:
    an experiment is multiple data collections by definition, since there's a
    basckground etc so each (what was componment) is actually a data collection?


    """

    def __init__(
        self,
        components,
        data_collections,
        simulations,
        background,
        transmission_maps=None,
    ):
        """the zeroth component is the  innermost. therfore a sample with no container
        will be :
            components = [powder]
            data_collections = [sample]
        and with 1:
            components = [powder, capillary
            data_colelctions = [sample, empty cap]
        etc.
        """
        self.components = components
        self.data_collections = data_collections
        self.simulations = simulations
        self.background = background
        if transmission_maps is None:
            # calculate the transmission maps
            pass
        self.transmission_maps = transmission_maps
        self.tmaps_sims = None
        self.tmaps_exps = None
        self.simulated_result = None
        self.experimental_result = None
        self._gain = 0  # these are just stored for the checker
        self._delta = 0  # these are just stored for the checker
        logging.info("Experiment object created")

    @classmethod
    def from_config(cls, json_file_path):
        # return cls()
        pass

    def __str__(self):
        i = 50
        line = "-" * i
        text = [line, "|{1:^{0}}|".format(i - 2, "Vaxadium Experiment"), line]
        text += ["Data Collections: {}".format(len(self.data_collections))]
        text += ["Components: {}".format(len(self.components))]
        text += ["Simulations: {}".format(len(self.simulations))]
        text += [line]
        return "\n".join(text)

    def __eq__(self, other):
        """
        two experiments are declared as equal if:
           1) the components are the same
           2) the simulations are the same
        """
        if type(self) is type(other):
            try:
                sims = [a == b for a, b in zip(self.simulations, other.simulations)]
                comp = [a == b for a, b in zip(self.components, other.components)]
                bools = sims + comp
                logger.debug(
                    "comparison of {} and {} --> {}".format(
                        self.__repr__(), other.__repr__(), bools
                    )
                )
                return all(bools)
            except IndexError:
                return False
        else:
            return False

    @property
    def n(self):
        return len(self.data_collections)

    @property
    def detector_shape(self):
        return self.data_collections[0].detector.n_pixels

    @property
    def all_data_collections(self):
        return [self.background] + self.data_collections

    @staticmethod
    def _map_transmission(sims_or_dcs, components, n_pixels, n_voxels, falsify=False):
        tmaps_obj = TransmissionMap(
            {"n_pixels": [n_pixels, n_pixels], "n_voxels": n_voxels}
        )
        t = sims_or_dcs[0]
        [component.add_beam(t.beam) for component in components]
        if not falsify:
            maps = tmaps_obj.calculate(components, t.beam, t.detector).transpose(
                (0, 1, 3, 2)
            )
        else:
            a = np.ones((2, 2))
            b = np.ones(t.detector.n_pixels)
            maps = a[..., None, None] * b[None, None, ...]
        return maps

    @property
    def sample(self):
        return self.components[0]

    @property
    def dc(self):
        return self.data_collections[0]

    def calc_transmission_maps(self, n_pixels=50, n_voxels=64, falsify=False):
        t0 = time.time()
        fake_bodge_components = deepcopy(self.components)
        fake_bodge_components[0].volume_fraction = 1
        self.tmaps_sims = self._map_transmission(
            self.simulations,
            fake_bodge_components,
            n_pixels,
            n_voxels,
            falsify,
        )
        self.tmaps_exps = self._map_transmission(
            self.data_collections,
            self.components,
            n_pixels,
            n_voxels,
            falsify,
        )
        proc_time = (time.time() - t0) * 1000
        proc = "falsified" if falsify else "calculated"
        logger.info("Transmission maps {} in {:6.4f} ms".format(proc, proc_time))

    @staticmethod
    def _do_preprocess(list_of_things_to_preprocess):
        for thing in list_of_things_to_preprocess:
            thing.preprocess()

    def do_simulation_preprocess(self):
        self._do_preprocess(self.simulations)

    def do_experimental_preprocess(self):
        raise DeprecationWarning
        self._do_preprocess(self.data_collections)

    def do_background_preprocess(self, set_pyfai=True):
        if set_pyfai:
            logger.debug("overwriting background pyfai with dc0")
            self.background.pyfai = self.data_collections[0].pyfai

    @staticmethod
    def _subtract_containers(sims_or_dcs, maps, also_correct_attenuation=False):
        if len(sims_or_dcs) == 1:
            logger.debug("no container to subtract...")
            if also_correct_attenuation:
                return sims_or_dcs[0].data / maps[0, 0]
            else:
                return sims_or_dcs[0].data
        else:
            container_attenuation_correction = maps[1, 0]
            thing = (
                sims_or_dcs[0].data
                - container_attenuation_correction * sims_or_dcs[1].data
            )
            if also_correct_attenuation:
                return thing / maps[0, 0] / maps[0, 1]
            else:
                return thing

    def do_simulation_container_subtraction(self, force=False):
        if self.simulated_result is None or force:
            self.simulated_result = self._subtract_containers(
                self.simulations, self.tmaps_sims, True
            )
            logger.info("simulation container subtraction complete")

    def do_experimental_container_subtraction(self):
        raise NotImplementedError
        self.experimental_result = self._subtract_containers(
            self.data_collections, self.tmaps_exps
        )
        logger.info("experimental container subtraction complete")

    def do_simulation_extraction(self, function="standard_bounded"):
        self.extractor = fitting.Extraction.from_library(function)
        self.extractor.fit(self.simulations[0].tth_chi_r, self.simulated_result)
        logger.debug("Simulation extraction complete. " + str(self.extractor))

    def do_interpolation(self):
        tth_chi_r = self.data_collections[0].tth_chi_r
        interpolated = self.extractor.interpolate(tth_chi_r)
        # apply the scaling to put into differential scattering cross section
        sample = self.components[0]
        sample_length_m = sample.path_length_canon([0, 0, 100]) / 100  # returns cm
        sample_rho = atom_number_density(sample.material, sample.density)
        scaled = (
            interpolated
            / sample_length_m
            / sample_rho
            / (PHYSICAL.ELECTRON_RADIUS**2).magnitude
        )
        logger.debug(
            "interpolating and scaling to length = {}, rho = {}".format(
                sample_length_m, sample_rho
            )
        )
        return scaled.reshape(self.detector_shape)
