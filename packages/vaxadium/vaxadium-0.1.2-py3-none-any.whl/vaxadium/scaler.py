import logging

import h5py as h5
import numpy as np
from pyFAI import units as pyFAIunits

from vaxadium.configuration import AXISKEYS, CONFIGKEYS, FORMFACTORKEYS
from vaxadium.constants import DATAKEYS as DKEYS
from vaxadium.core.axis_generators import generate_axis, get_ai_params
from vaxadium.core.form_factors import sum_of_f2
from vaxadium.io.outputs import default_outputs
from vaxadium.physics import (
    atom_number_density,
    g0_minus_one,
    krogh_moe_sum_from_formula,
    thomson_dscs,
)

logger = logging.getLogger(__name__)


class ScaledResult:
    """
    A ScaledResult is the holder of the result from a single Experiment.
    it has a differential scattering cross section ready for further maths fun.
    """

    def __init__(self, q_inst, dscs, rho, g0_minus_1):
        self.q_inst = q_inst
        self.dscs = dscs
        self.rho = rho
        self.g0_minus_1 = g0_minus_1
        self.configuration = {}
        self.r = None

    @classmethod
    def from_experiment(cls, q, dscs, experiment, g0_minus_1):
        # calculate rho and g0_minus_1 from the expeiment object
        sample = experiment.components[0]
        rho = atom_number_density(sample.material, sample.density) / 1e30
        return cls(q, dscs, rho, g0_minus_1)


class ScaledResultCollectionIterator:
    def __init__(self, collection):
        self.collection = collection
        self._index = 0

    def __next__(self):
        if self.collection.n == 0:
            logger.warn("Iterating over scaled results collection with  no data points")
        if self._index < self.collection.n:
            axes, result = (
                self.collection.axis_values[self._index],
                self.collection.results[self._index],
            )
            self._index += 1
            return axes, result
        raise StopIteration


class ScaledResultsCollection:
    """
    A ScaledResultsCollection is a collection of scaled results and is invoked
    when an experiment runner creates scaled results..
    It provides a useful way of tracking axis data, and for applying axis-dependant
    processing where requried.

    """

    def __init__(self, configuration):
        self.configuration = configuration
        self.results = []
        self.axis_values = []
        # globally used parameters
        r = np.arange(
            configuration[CONFIGKEYS.RMINFT],
            configuration[CONFIGKEYS.RMAX],
            configuration[CONFIGKEYS.RSTEP],
        )
        q_inst = generate_axis(
            configuration[CONFIGKEYS.QMIN],
            configuration[CONFIGKEYS.QMAX_INST],
            configuration[CONFIGKEYS.QSTEP],
        )

        itrunc = np.searchsorted(q_inst, configuration[CONFIGKEYS.QMAX])
        q = q_inst[:itrunc]

        self.configuration[AXISKEYS.Q] = q
        self.configuration[AXISKEYS.Q_INST] = q_inst
        self.configuration[AXISKEYS.ITRUNC] = itrunc
        self.configuration[AXISKEYS.R] = r

        self._nxs_filepath = None
        self.outputs = default_outputs

    def __iter__(self):
        return ScaledResultCollectionIterator(self)

    def __getitem__(self, val):
        return self.results[val]

    @property
    def n(self):
        len_data = len(self.results)
        len_axes = len(self.axis_values)
        if len_data != len_axes:
            logger.warning(
                "inconsitent length of axes and data in {}".format(self.__class__)
            )
        return len_data

    def apply(self, function):
        """applies a function to every scaled result in the collection"""
        for result in self.results:
            function(result)

    def _open_nxs_file(self):
        self._nxs = h5.File(self._nxs_filepath, "w", libver="latest")
        self._nxentry = self._nxs.create_group("vaxadium")
        self._nxentry.attrs["NX_class"] = "NXentry"

    def _close_nxs_file(self):
        self._nxs.close()

    def _setup_writing(self, filepath, outputs, swmr=False):
        """Set up the file for saving.
        A new hdf5 file is established, with a dataset created for each of the outputs.
        outputs should be a list of Dataxis objects
        if swmr is True, the file is opened in swmr mode and handle is left open
        if swmr is false, then the file is still left open but not in swmr mode
        """
        self._nxs_filepath = filepath
        self._open_nxs_file()
        self.outputs = outputs
        for output in self.outputs:
            output.create_dataset(self._nxentry, self.configuration)
        if swmr:
            # this rather strange concoction is because of...
            # ValueError: It is not possible to forcibly switch SWMR mode off.
            self._nxs.swmr_mode = swmr

    def _write_result(self, result):
        for output in self.outputs:
            output._partial_write(result)

    def _write(self, slice="all"):
        """go through all the outputs in self._outputs and tell them to retrieve
        their data and write/update their datasets

        this is called by users

        so it needs to init everything, get the data, and then close the file.

        how doe sit know which outputs to put in the list?
        """

        if slice == "all":
            for result in self.results:
                self._write_result(result)
        elif isinstance(slice, int):
            self._write_result(self.results[slice])
        else:
            logger.warning(
                "_write method called with unusable argument {}".format(slice)
            )

    def write(self, filepath, outputs=None):
        """write all of the outputs. intended for human use"""
        outputs = outputs or self.outputs
        self._setup_writing(filepath, outputs)
        self._write()
        self._close_nxs_file()

    def save(self, filepath=None):
        """this is intended more as a state-save than an output-save."""
        pass

    def add_scaled_experiment(self, axis_value, scaled, save=False):
        assert isinstance(axis_value, dict), "axis_value should be a dict"
        # do some things
        self.axis_values.append(axis_value)
        self.results.append(scaled)
        if save:
            self.save()

    def process(self, slice=None):
        """
        process runs the results in scaled through the as-defined process
        updates self.sofq, self.dofr, etc.
        """
        pass


class illDefinedExperimentException(Exception):
    pass


def scale_experiment(experiment, configuration):
    # do something to the experiment
    # this function requires that the experiment has been suitably preprocessed.
    # we check that here before proceeding.
    if experiment.tmaps_exps is None:
        raise illDefinedExperimentException("no tmaps_exps on experiment")
    if experiment.extractor is None:
        raise illDefinedExperimentException("no extractor object on experiment")
    # if experiment.extractor.r_squared is None:
    #    raise illDefinedExperimentException('no successful extractor on experiment')

    # check there are no borked keys in configuration
    allowed_keys = [b for a, b in vars(CONFIGKEYS).items() if not a.startswith("__")]
    allowed_keys += [b for a, b in vars(AXISKEYS).items() if not a.startswith("__")]

    keys_for_removal = []
    logger.debug(configuration)
    for k in configuration.keys():
        if k not in allowed_keys:
            logger.warning(
                "unexpected key in user configuration. "
                'Ignoring the supplied key "{}"'.format(k)
            )
            keys_for_removal.append(k)
    for badkey in keys_for_removal:
        del configuration[badkey]
    # lock the dict
    # configuration = LockedDict(configuration)

    # interpolate simulation data onto experiment detector
    interpolated = experiment.do_interpolation()

    # we need q to scale the experiment
    q, ai_range, ai_npts = get_ai_params(
        configuration[CONFIGKEYS.QMIN],
        configuration[CONFIGKEYS.QMAX_INST],
        configuration[CONFIGKEYS.QSTEP],
    )
    # normalise by flux
    # TODO either read the i0 from the file along with the data, or accept a
    # configuration key for this
    for dc in experiment.all_data_collections:
        dc.apply(lambda x: x / dc.beam.normalisation, DKEYS.NORMIO)

    # normalise to solid angle
    for dc in experiment.all_data_collections:
        dc.apply(lambda x: x / dc.solid_angle, DKEYS.SOLID_ANGLE)

    # subtract empty beamline from all data collections
    for dc in experiment.data_collections:
        dc.apply(lambda x: x - experiment.background.data, DKEYS.SUBBAK)

    # calculate / get the transmission maps? and formulate corrections.
    # case 1 is just a sample and no containers
    if experiment.n == 1:
        container_attenuation_correction = np.ones_like(experiment.dc.data)
        sample_attenuation_correction = experiment.tmaps_exps[0, 0, :, :]

        experiment.dc.set_new_data(experiment.dc.data.squeeze(), DKEYS.SUBCAP)
    elif experiment.n == 2:
        container_attenuation_correction = experiment.tmaps_exps[1, 0]
        sample_attenuation_correction = (
            experiment.tmaps_exps[0, 0] * experiment.tmaps_exps[0, 1]
        )
        dcs = experiment.data_collections
        subcap = dcs[0].data - dcs[1].data * container_attenuation_correction
        dcs[0].set_new_data(subcap, DKEYS.SUBCAP)
    else:
        logger.error("not yet")
        raise NotImplementedError("not implemented the logic for this yet")

    # generically prepare for iteration
    det_trans_corr = 1 - experiment.dc.detector_transmission

    thomson = thomson_dscs(experiment.dc.tth, experiment.dc.chi)
    k_m = krogh_moe_sum_from_formula(
        experiment.sample.density, experiment.sample.material
    )
    initial_gain = configuration[CONFIGKEYS.GAIN]
    gain = initial_gain
    logger.info("starting refinement of the gain. g0 = {}".format(initial_gain))

    for ranges in [
        0.000001,
        0.000001,
        0.000001,
        0.000001,
        0.000001,
        0.000001,
        0.000001,
        0.000001,
        0.000001,
        0.000001,
        0.000001,
        0.000001,
    ]:
        potential_gains = [gain * (1 - ranges), gain * (1 + ranges)]
        gain_calculator = two_point_iteration(
            experiment,
            potential_gains,
            q,
            interpolated,
            det_trans_corr,
            sample_attenuation_correction,
            thomson,
            k_m,
            configuration,
            ai_npts,
            ai_range,
        )
        gain = gain_calculator(k_m)

    # ITERATE
    qsq = result = None
    for i in range(1, configuration[CONFIGKEYS.ITERATIONS] + 1):
        gain, result, qsq = iterate(
            i,
            experiment,
            gain,
            q,
            interpolated,
            det_trans_corr,
            sample_attenuation_correction,
            thomson,
            k_m,
            configuration,
            ai_npts,
            ai_range,
        )
        logger.info(
            (
                "fine iteration of gain. gain = "
                "{:14.3f}, Q·S(Q) = {:10.8f}, k_m = {:10.8f}; Δ = {: 10.8f}".format(
                    gain, qsq, k_m, qsq - k_m
                )
            )
        )

    logger.info("Iteration Complete. gain = {}".format(gain))
    configuration[CONFIGKEYS.GAIN_RESULT] = gain
    experiment._gain = gain
    experiment._delta = qsq - k_m

    logger.info("Normalising to {}".format(configuration[CONFIGKEYS.FSQUARED]))
    foq = sum_of_f2(q, experiment.sample.material, configuration[CONFIGKEYS.FSQUARED])
    experiment.dc._data["foq"] = foq
    scaled_result = result / foq
    g0_minus_1 = (
        g0_minus_one(experiment.sample.material)
        if configuration[CONFIGKEYS.FSQUARED] == FORMFACTORKEYS.SQUAREOFSUMS
        else 1
    )
    scaled = ScaledResult.from_experiment(q, scaled_result, experiment, g0_minus_1)

    return scaled


def two_point_iteration(
    experiment,
    gains,
    q,
    interpolated,
    det_trans_corr,
    sample_attenuation_correction,
    thomson,
    k_m,
    configuration,
    pyfai_inst_npts,
    pyfai_inst_range,
):
    results = []
    for i, point in enumerate(gains):
        _, _, qsq = iterate(
            i,
            experiment,
            point,
            q,
            interpolated,
            det_trans_corr,
            sample_attenuation_correction,
            thomson,
            k_m,
            configuration,
            pyfai_inst_npts,
            pyfai_inst_range,
        )
        results.append(qsq)

    dx = gains[1] - gains[0]
    dy = results[1] - results[0]

    def gain_calculator(qsq):
        result = ((qsq - results[0]) * dx / dy) + gains[0]
        logger.info(
            "calculating new gain of {} for qsq of {} (dx:{}; dy:{})".format(
                result, qsq, dx, dy
            )
        )
        return result

    return gain_calculator


def iterate(
    i,
    experiment,
    gain,
    q,
    interpolated,
    det_trans_corr,
    sample_attenuation_correction,
    thomson,
    k_m,
    configuration,
    pyfai_inst_npts,
    pyfai_inst_range,
):
    #    scale the subcap
    scaled_real = experiment.dc._data[DKEYS.SUBCAP] / (
        gain * 5 * experiment.sample.path_length_canon([0, 0, 100]) / 100
    )  # 5 makes the starting value 1e9

    #    subtract the interpolated from the data
    subtracted = (
        (scaled_real - interpolated)
        / det_trans_corr
        / sample_attenuation_correction
        / thomson
    )

    experiment.dc._data["test"] = (
        scaled_real / det_trans_corr / sample_attenuation_correction
    )
    experiment.dc._data["test2"] = (
        interpolated / det_trans_corr / sample_attenuation_correction
    )

    #    integrate to 1d
    iterated_result = experiment.dc.pyfai.integrate1d(
        subtracted,
        pyfai_inst_npts,
        correctSolidAngle=False,
        unit=pyFAIunits.Q_A,
        radial_range=pyfai_inst_range,
        polarization_factor=configuration[CONFIGKEYS.POLARIZATION],
    )
    #    qsq integral
    numerator = iterated_result[1]
    qsq_integral = np.trapz(numerator * q**2, x=q)

    #    correct the previous scale factor
    gain = gain + 10 * (qsq_integral - k_m)

    return gain, numerator, qsq_integral
