import json
import logging
from pathlib import Path

from vaxadium.checks import run_diagnostics_checks
from vaxadium.configuration import CKEYS, VaxadiumConfigurationError, defaultconfig
from vaxadium.constants import NEWG4NEXUSKEYS, NEWNXXPDFNEXUSKEYS, NEWNXXPDFNEXUSKEYSBKG
from vaxadium.experiment import Experiment
from vaxadium.io.nexus_reader import (
    NexusReaderPyFAI,
    NexusReaderPyFAISample,
    NxxpdfReader,
)
from vaxadium.io.outputs import default_outputs
from vaxadium.io.serializer_factory import SERIALIZERS, nexus_serializer
from vaxadium.processors import FourierTransformer, TopHatter
from vaxadium.scaler import ScaledResultsCollection, scale_experiment

logger = logging.getLogger(__name__)


def get_config_from_file(filepath):
    filepath = Path(filepath)
    try:
        with open(filepath.expanduser().absolute(), "r") as f:
            config = json.load(f)
            return config
    except FileNotFoundError as e:
        print("config path wrong")
        logger.error("could not open config file {}".format(filepath) + str(e))
        return {}


class ExperimentRunner:
    def __init__(
        self,
        nxs_file=None,
        simulations=None,
        background=None,
        data_collections=None,
        components=None,
        transmission_maps=None,
        config=dict(),
    ):
        self.nxs = nxs_file
        self.simulations = simulations or []
        self.background = background
        self.data_collections = data_collections or []
        self.components = components or []
        self.transmission_maps = transmission_maps or []
        self.configuration = {**defaultconfig, **config}
        self.experiment = None
        self._output_filepath = None
        self._outputs = default_outputs
        self._diagnostics_filepath = ""
        self._diagnostics_results = list()
        self.n_pixels_for_tmaps = 20
        self.n_voxels_for_tmaps = 64

    @classmethod
    def from_configuration_dictionary(cls, config):
        logger.debug("configuration: {}".format(config))
        # check there are no erronious empty file paths in the config
        if config.get("background") == "":
            raise VaxadiumConfigurationError(
                "background filepath supplied is empty string"
            )
        for k, v in config.items():
            if k == CKEYS.SAMPLE or "container" in k:
                if v.get("dc") == "":
                    raise VaxadiumConfigurationError(
                        "{} filepath supplied is empty string".format(k)
                    )
        runner = cls(config=config.get("configuration", {}))
        try:
            bkg_fp = config[CKEYS.BACKGROUND]
        except KeyError:
            logger.error("No background found in config")
        bkg_nxs = NexusReaderPyFAI(NEWNXXPDFNEXUSKEYSBKG)
        bkg_nxs.read(bkg_fp)
        runner.background = nexus_serializer.serialize(bkg_nxs, SERIALIZERS.BACKGROUND)

        # get the sample paths from the config
        runner.nxs = runner._add_dc_and_sim(config[CKEYS.SAMPLE], CKEYS.SAMPLE)

        # Now count the container nxs files and retrieve info
        for i in range(10):
            for k, v in config.items():
                if str(i) in k:
                    try:
                        _ = runner._add_dc_and_sim(v, k, True)
                    except KeyError as e:
                        logger.error(
                            "Could not read data for key {}".format(k) + str(e)
                        )

        runner.construct_experiment()

        return runner

    @classmethod
    def from_json(cls, filepath):
        logger.debug("configuration file path: {}".format(filepath))
        config = get_config_from_file(filepath)
        return cls.from_configuration_dictionary(config)

    @property
    def n_points(self):
        return self.nxs.n_points

    def construct_experiment(self):
        self.experiment = Experiment(
            self.components,
            self.data_collections,
            self.simulations,
            self.background,
            None,
        )
        self._preprocessed = False

    def set_output_file(self, filepath):
        """output filepath will be a nxs file in which everything will be saved."""
        self._output_filepath = Path(filepath)

    def set_diagnostics_file(self, filepath):
        """json file in which the diagnostics will be saved."""
        if filepath:
            self._diagnostics_filepath = Path(filepath)

    def do_diagnostics_checks(self):
        """run checkers against the current experiment, then dump contents into file"""
        logger.debug("running diagnostics")
        diagnostics_header = {"level": -1, "filepath": str(self.nxs.filename)}
        self._diagnostics_results = [diagnostics_header] + run_diagnostics_checks(
            self.experiment
        )
        logger.debug(self._diagnostics_results)
        if self._diagnostics_filepath:
            logger.debug(
                "attempting to write diagnostics to file {}".format(
                    self._diagnostics_filepath
                )
            )
            with open(self._diagnostics_filepath, "w") as f:
                f.write(json.dumps(self._diagnostics_results, indent=4))

    def _format_diagnostics_results(self, verbose=False):
        icons = ["✓", "!!", "XXX"]
        lines = []
        for t in self._diagnostics_results:
            if t["level"] == -1:
                continue
            if verbose:
                lines.append(
                    "{:5} | {:100} \n{}".format(
                        icons[t["level"]], t["text"], t["summary"]
                    )
                )
            else:
                lines.append("{:5} | {:100}".format(icons[t["level"]], t["text"]))
        return lines

    def print_diagnostics_results(self, verbose=False):
        lines = self._format_diagnostics_results(verbose)
        for line in lines:
            print(line)

    def log_diagnostics_results(self, verbose=False):
        lines = self._format_diagnostics_results(verbose)
        for line in lines:
            logger.info(line)

    def _add_dc_and_sim(self, dict_of_paths, k="", load_data=False):
        """This method exists so that the similation and data collection can
        be added together. This is necessary because the sim has no concept of
        detector efficiency and therefore sensor material, density, etc. This
        method copies the sensor info from the dc and applies it to the sim.
        """
        logging.debug("dict_of_paths = {}".format(dict_of_paths))
        sensor = {}
        # get the dc filepath from the dixt
        if not dict_of_paths:
            msg = "missing file/s in configuration: {}".format(k)
            logging.error(msg)
            raise VaxadiumConfigurationError(msg)
        try:
            dc_fp = dict_of_paths[CKEYS.DATACOLLECTION]
        except KeyError:
            msg = 'no "dc" key in {}'.format(k)
            logger.error(msg)
            raise VaxadiumConfigurationError(msg)

        logger.info("Getting data collection metadata from " + str(dc_fp))

        # construct nxs reader
        dc_nxs = NxxpdfReader(NEWNXXPDFNEXUSKEYS)
        dc_nxs.read(dc_fp)

        # serialize nxs reader into components and then data collections
        try:
            self.components += [
                nexus_serializer.serialize(dc_nxs, SERIALIZERS.ATTENUATORS)[0]
            ]
        except IndexError:
            logger.error("Incomplete sample metadata in {}".format(dc_fp))
        try:
            dc = nexus_serializer.serialize(dc_nxs, SERIALIZERS.DATACOLLECTIONS)[0]
            if load_data:
                dc.set_raw_data(dc_nxs.read_data())
            dc.name = k
            sensor = dc.detector.sensor
            self.data_collections += [dc]
        except IndexError:
            logger.error("Incomplete data collection metadata in {}".format(dc_fp))

        # get the sim filepath from the dict
        sim_fp = None
        try:
            sim_fp = dict_of_paths[CKEYS.SIMULATION]
        except KeyError:
            logger.error('no "sim" key in {}'.format(k))

        logger.info("Getting simulation data from " + str(sim_fp))

        # construct nxs reader
        sim_nxs = NexusReaderPyFAISample(NEWG4NEXUSKEYS)
        sim_nxs.read(sim_fp)

        # serialize into simulation object
        try:
            sim = nexus_serializer.serialize(sim_nxs, SERIALIZERS.SIMULATION)
            sim.detector.apply_params(sensor)
            self.simulations += [sim]
        except Exception as e:
            logger.error(
                (
                    "There was an uncaught error reading the simulation data "
                    "from {}: {}".format(sim_fp, e)
                )
            )

        return dc_nxs

    def prepare_to_run(self, force=False):
        """
        prepare to call run. This mostly involves getting the extracted numbers,
        calculating the tmaps, etc every axtion of this function is checked by an
        assert in the scale_experimebnt fuicntions (it should not be, obvs)

        recall that the thing you want to fit is the sample sim, having been
        correcrted for detector effects and photoins and solid angle, having had the
        equivalent capillary sim subtracted from it. should perhaps
        also correct the simulation for self-attenuation before extraction...
        #TODO think about this!
        """
        self.experiment.calc_transmission_maps(
            n_pixels=self.n_pixels_for_tmaps,
            n_voxels=self.n_voxels_for_tmaps,
            falsify=False,
        )
        self.experiment.do_simulation_preprocess()
        self.experiment.do_simulation_container_subtraction(force=force)
        self.experiment.do_simulation_extraction()
        self.experiment.do_background_preprocess()
        self._preprocessed = True

    def run(self):
        logger.info("running...")
        # check the background is present

        if self.experiment is None:
            logger.warning("no experiment constructed, creating..")
            self.construct_experiment()
        if not self._preprocessed:
            logger.debug("preprocessing required")
            self.prepare_to_run()
        scaled_results = ScaledResultsCollection(self.configuration)
        self.procs = prepare_procs(scaled_results)

        if self._output_filepath is not None:
            # then we save each point as we go
            save_as_we_go = True
            # set up the file writer
            scaled_results._setup_writing(self._output_filepath, self._outputs, True)
        else:
            save_as_we_go = False

        for axisn, axisv, data in self.nxs:
            self.experiment.data_collections[0].set_raw_data(data)
            scaled_experiment = scale_experiment(self.experiment, self.configuration)
            [x(scaled_experiment) for x in self.procs]
            axis = {k: v for k, v in zip(axisn, [axisv])}
            scaled_results.add_scaled_experiment(axis, scaled_experiment, save_as_we_go)
            scaled_results.process()

        logger.info("running complete.")
        if self._diagnostics_filepath != "":
            try:
                logger.info("running diagnostics...")
                self.do_diagnostics_checks()
            except Exception as e:
                logger.error("there was an error running the diagnostics")
                logger.error(e)
        return scaled_results

    def change_sample_composition(self, composition):
        self.experiment.components[0].material = composition
        self._preprocessed = False


def prepare_procs(collection):
    logger.debug("preparing processors from {}.".format(collection))
    top_hatter = TopHatter.from_collection(collection)
    transformer = FourierTransformer.from_collection(collection)
    return [top_hatter, transformer]
