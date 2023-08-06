import logging
from functools import singledispatch
from pathlib import Path

import h5py
import numpy as np
import xraylib
from pyFAI.azimuthalIntegrator import AzimuthalIntegrator
from pyFAI.detectors import Detector as PDetector

from vaxadium.configuration import VaxadiumException
from vaxadium.constants import KEYS, NexKey
from vaxadium.core.units import Q_

logger = logging.getLogger(__name__)


@singledispatch
def get_units(arg):
    return arg


@get_units.register
def _(arg: bytes):
    return arg.decode()


@singledispatch
def get_value(arg):
    return arg


@get_value.register
def _(arg: bytes):
    return arg.decode()


@get_value.register
def _(arg: np.ndarray):
    if len(arg) == 1:
        return get_value(arg[0])
    elif isinstance(arg[0], bytes):  # who puts an isinstance in a singledispatch
        return arg.astype(str)
    else:
        return arg


class VanillaNexusReader(object):
    def __init__(self, nodes):
        self.f = None
        self.params = {}
        self.nodes = nodes
        self.additional_serializers = []
        self.additional_readers = []

    def _open(self, filename, swmr):
        logging.debug("opening {} with swmr={}".format(filename, swmr))
        self.filename = filename
        try:
            self.f = h5py.File(filename, "r", swmr=swmr)
        except OSError:
            logger.error("File could not be opened {}".format(filename))
            raise

    def _close(self):
        logging.debug("closing file")
        self.f.close()

    def _read(self):
        logger.debug("_reading")
        nexus_keys = self.nodes.get_keys()
        for k, v in nexus_keys.items():
            self._add_param_to_params(k, v)
            if not v.bothered and self.params[k] is None:
                logger.info(
                    "key {} not present or needed, removing from params".format(k)
                )
                del self.params[k]

    def _apply_lambdas(self):
        logging.debug("applying lambda keys")
        lambdas = self.nodes.get_lambdas()
        for k, l in lambdas.items():
            self.params[k] = l(self.params)

    def serialize(self, serializer):
        logging.debug("serialize method called on {}".format(self.__class__))
        serializer.start_object("whatever")
        serializer.add_property(KEYS.SOURCE_FILE, self.filename)
        for k, v in self.params.items():
            serializer.add_property(k, v)
        for s in self.additional_serializers:
            s(serializer)

    def read(self, filename, swmr=False):
        filename_path = Path(filename).expanduser().absolute()
        self._open(filename_path, swmr)
        self._read()
        self._apply_lambdas()
        for reader in self.additional_readers:
            reader()
        self._close()

    def _get_node(self, address):
        logging.debug("getting node {} from {}".format(address, self.filename))
        if not bool(self.f):
            logger.error("Attempted to read node from closed hdf5 file object")
            raise IOError("hdf5 file object is closed")
        try:
            node = self.f[address]
        except KeyError:
            return False
        logging.debug(node)
        return node

    def _read_node(self, nexkey):
        node = self._get_node(nexkey.address)
        if node is False:
            if nexkey.bothered:
                logger.warning(
                    "Node expected at {} not found in file {}.".format(
                        nexkey.address, self.filename
                    )
                )
            return
        value = get_value(node[()])
        units = None
        if "units" in node.attrs.keys():
            units = get_units(node.attrs["units"])
        elif nexkey.unit_required:
            units = nexkey.default_unit
            logger.warning(
                "Node requires units but none present at {}. Using default ({})".format(
                    nexkey.address, units
                )
            )

        if units is None:
            return value
        else:
            return Q_(value, units)

    def _add_param_to_params(self, key, nexkey):
        param = self._read_node(nexkey)
        self.params[key] = param

    def _read_axes_from_node(self, address):
        node = self._get_node(address)
        if "axes" in node.attrs.keys():
            axes_labels = get_value(node.attrs["axes"])[
                :-2
            ]  # -2 so as to avoid x and y
            axes_values = []
            for label in axes_labels:
                axis_values = self._read_node(NexKey(address + "/" + label))
                try:
                    # TODO https://github.com/hgrecco/pint/issues/1195
                    a = axis_values.tolist()
                    axes_values.append(a)
                except TypeError:
                    axes_values.append([axis_values])
                except AttributeError:
                    axes_values.append([axis_values])
            return axes_labels, axes_values
        else:
            return None, None

    def _get_number_of_members(self, address):
        try:
            n = len(self.f[address].keys())
        except KeyError:
            logger.debug(
                "cannot get number of members of {}, assuming n=0".format(address)
            )
            n = 0
        return n

    def search(self, target, values_also=True):
        """a helpful fucntion to find the params that match the target string"""
        for k, v in self.params.items():
            if target in k:
                if values_also:
                    print("{:25s} {}".format(k, v))
                else:
                    print(k)


class InsufficientPyfaiException(VaxadiumException):
    pass


class NexusReaderPyFAI(VanillaNexusReader):
    def __init__(self, nodes):
        super().__init__(nodes)
        self.pyfai = AzimuthalIntegrator()
        self.additional_serializers.append(self._serialize_pyfai)
        self.additional_readers.append(self._update_pyfai_from_params)

    def _update_pyfai_from_params(self, filepath=None):
        logging.debug("updating pyfai")
        if filepath is None:
            # update from self.params
            try:
                poni_fp = self.params["detector_poni_filepath"]
                if poni_fp == "":
                    logger.warning("no poni filepath found in file")
                    raise KeyError("no poni filepath found in file")
                self.pyfai.load(poni_fp)
            except KeyError as ke:
                try:
                    logging.info(
                        "attempting to construct poni from metadata since {}".format(ke)
                    )
                    # take a guess from the parameters
                    data_shape = self.params[KEYS.DATA].shape[-2:]
                    pixel_x = (
                        2
                        * self.params[KEYS.DETECTOR_HALF_X].to("m").magnitude
                        / data_shape[1]
                    )
                    pixel_y = (
                        2
                        * self.params[KEYS.DETECTOR_HALF_Y].to("m").magnitude
                        / data_shape[0]
                    )
                    logger.debug("pixel_x: {}; pixel_y:{}".format(pixel_x, pixel_y))
                    self.pyfai.detector = PDetector(
                        pixel1=pixel_x, pixel2=pixel_y, max_shape=data_shape
                    )
                    self.pyfai.set_dist(
                        self.params[KEYS.DETECTOR_DISTANCE].to("m").magnitude
                    )
                    self.pyfai.set_poni1(
                        self.params[KEYS.DETECTOR_HALF_X].to("m").magnitude
                    )
                    self.pyfai.set_poni2(
                        self.params[KEYS.DETECTOR_HALF_Y].to("m").magnitude
                    )
                    self.pyfai.set_wavelength(
                        self.params[KEYS.PRIMARY_BEAM_WAVELENGTH].to("m").magnitude
                    )
                except Exception as e:
                    logging.exception(e)
                    raise InsufficientPyfaiException(
                        (
                            "No poni file and no compatible detector configuration "
                            "found in {}".format(self.filename)
                        )
                    )
        else:
            self.pyfai.load(filepath)

    def _serialize_pyfai(self, serializer):
        if self.pyfai.get_shape() is None:
            raise InsufficientPyfaiException(
                "Cannot get pyfai poni file from {}".format(self.filename)
            )
        serializer.add_property(KEYS.DETECTOR_PONI1, Q_(self.pyfai.get_poni1(), "m"))
        serializer.add_property(KEYS.DETECTOR_PONI2, Q_(self.pyfai.get_poni2(), "m"))
        serializer.add_property(
            KEYS.DETECTOR_ROT1, Q_(self.pyfai.get_rot1(), "radians")
        )
        serializer.add_property(
            KEYS.DETECTOR_ROT2, Q_(self.pyfai.get_rot2(), "radians")
        )
        serializer.add_property(
            KEYS.DETECTOR_ROT3, Q_(self.pyfai.get_rot3(), "radians")
        )
        serializer.add_property(
            KEYS.DETECTOR_PYFAI_DIST, Q_(self.pyfai.get_dist(), "m")
        )
        serializer.add_property(
            KEYS.DETECTOR_UI, Q_(tuple(-self.pyfai.rotation_matrix()[0]))
        )
        serializer.add_property(
            KEYS.DETECTOR_UK, Q_(tuple(-self.pyfai.rotation_matrix()[2]))
        )
        origin = np.array(self.pyfai.calc_pos_zyx(corners=True))
        serializer.add_property(KEYS.DETECTOR_ORIGIN, Q_(origin[::-1, -1, -1, 2], "m"))


class NexusReaderSample(VanillaNexusReader):
    def __init__(self, nodes):
        super().__init__(nodes)
        self.additional_readers.append(self._complete_sample_information)

    def _complete_sample_information(self):
        for i in range(self.params["number_of_samples"]):
            logging.debug("adding sample {}".format(i))
            if "sample{}_atoms".format(i) not in self.params.keys():
                formula = self.params["sample{}_formula".format(i)]
                logging.debug(formula)
                atoms, mass_fractions = self._convert_formula_to_mass_fractions(formula)
                self.params["sample{}_atoms".format(i)] = atoms
                self.params["sample{}_mass_fractions".format(i)] = mass_fractions
            elif "sample{}_formula".format(i) not in self.params.keys():
                logging.debug(self.params["sample{}_atoms".format(i)])
                atoms = self.params["sample{}_atoms".format(i)]
                atoms = [atoms] if type(atoms) is not np.ndarray else atoms
                mass_fractions = self.params["sample{}_mass_fractions".format(i)]
                mass_fractions = (
                    [mass_fractions]
                    if type(mass_fractions) is not np.ndarray
                    else mass_fractions
                )
                formula = self._convert_mass_fractions_to_formula(atoms, mass_fractions)
                self.params["sample{}_formula".format(i)] = "".join(formula)

    @staticmethod
    def _convert_mass_fractions_to_formula(atoms, mass_fractions):
        logging.debug(
            "convert mass fractions to formula: {}; {}".format(atoms, mass_fractions)
        )
        atomic_weights = [
            xraylib.AtomicWeight(xraylib.SymbolToAtomicNumber(x)) for x in atoms
        ]
        molar_fractions = np.array(
            [mass / weight for (weight, mass) in zip(atomic_weights, mass_fractions)]
        )
        formula = [
            "{}{:.5f}".format(sym, num)
            for (sym, num) in zip(atoms, molar_fractions / molar_fractions.min())
        ]
        return formula

    @staticmethod
    def _convert_formula_to_mass_fractions(formula):
        xrl_compound = xraylib.CompoundParser(formula)
        atoms = [xraylib.AtomicNumberToSymbol(x) for x in xrl_compound["Elements"]]
        mass_fractions = xrl_compound["massFractions"]
        return atoms, mass_fractions


class NexusDataIterator:
    def __init__(self, nxs):
        self._nxs = nxs
        self._index = 0

    def __next__(self):
        if self._nxs.n_points == 0:
            logger.warn("Iterating over nxs handler with no data points")
        if self._index < self._nxs.n_points:
            axis_names, axis_values, result = self._nxs.read_data_and_axes(self._index)
            self._index += 1
            return axis_names, axis_values, result
        raise StopIteration


class NexusReaderIterable(VanillaNexusReader):
    def __init__(self, nodes):
        super().__init__(nodes)
        self.n_points = 0
        self.additional_readers.append(self._update_n_points)

    def __iter__(self):
        return NexusDataIterator(self)

    def _update_n_points(self):
        try:
            n = len(self.params["unique_keys"])  # TODO how appropriate is this?
        except TypeError:
            # ducktype that this is an int, so it's one frame
            n = 1
        self.n_points = n

    def read_data(self, frame=0, swmr=False):
        logger.info("loading data slice {} from {}".format(frame, self.filename))
        self._open(self.filename, swmr)
        data = self.f[self.nodes._DATA][frame]
        self._close()
        return data

    def read_data_and_axes(self, frame=0, swmr=False):
        logger.info("loading data slice {} from {}".format(frame, self.filename))
        self._open(self.filename, swmr)
        data = self.f[self.nodes._DATA][frame]
        axis_names, axis_value = self._read_axes_from_node(
            self.nodes._DETECTOR_FOR_AXES
        )
        self._close()

        logger.info(
            "axis name/s: {}, axis value = {}".format(
                axis_names[0], axis_value[0][frame]
            )
        )
        return axis_names, axis_value[0][frame], data


class NxxpdfReader(NexusReaderPyFAI, NexusReaderSample, NexusReaderIterable):
    pass


class NexusReaderPyFAISample(NexusReaderPyFAI, NexusReaderSample):
    pass
