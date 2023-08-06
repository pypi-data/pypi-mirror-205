import logging
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from vaxadium.configuration import AXISKEYS, MAX_NXS_SHAPE

logger = logging.getLogger(__name__)


@dataclass
class Outputter:
    axis_name: str
    axis_unit: str
    data_name: str
    also_txt: bool = False
    suffix: str = "xy"

    def __post_init__(self):
        self.nxdata = None
        self.n = 0
        self.dim0 = 0

    @property
    def filepath(self):
        if self.nxdata is None:
            return ""
        else:
            return self.nxdata.file.filename

    def create_dataset(self, nxentry, config):
        # need to discover the length of the axis
        self.axis = config[self.axis_name]
        self.dim0 = self.axis.shape[0]

        logger.info(
            "creating dataset {} in file {} with shape {}".format(
                self.data_name, self.filepath, self.dim0
            )
        )

        # create the group
        nxdata = nxentry.create_group(self.data_name)
        nxdata.attrs["NX_class"] = "NXdata"
        nxdata.attrs["signal"] = self.data_name
        nxdata.attrs["axes"] = self.axis_name
        nxdata.attrs["{}_indices".format(self.axis_name)] = [
            0,
        ]

        # add the axis
        nxaxis = nxdata.create_dataset(self.axis_name, data=self.axis)
        nxaxis.attrs["units"] = self.axis_unit

        # set the dataset
        self.nxdata = nxdata.create_dataset(
            self.data_name, shape=(self.dim0, 0), maxshape=(self.dim0, MAX_NXS_SHAPE)
        )

        # TODO sort this mess out
        self.nxdata.attrs["units"] = "counts"

    def _partial_write(self, scaled_result):
        logger.debug("_partial write called for {}".format(self.data_name))
        new_shape = (self.dim0, self.n + 1)
        self.nxdata.resize(new_shape)
        data = getattr(scaled_result, self.data_name)
        self.nxdata[:, -1] = data
        self.nxdata.flush()

        if self.also_txt:
            self._write_txt_file(data)

        self.n += 1

    def _get_xy_filepath(self, filepath):
        p = Path(filepath)
        return p.parent / (
            p.stem + "_" + self.data_name + "_{:03d}".format(self.n) + "." + self.suffix
        )

    @staticmethod
    def _get_xy_array(axis, data):
        return np.c_[axis, data]

    def _write_txt_file(self, data):
        logger.debug(
            "_write_txt_file called for {} with data of shape {}".format(
                self.data_name, data.shape
            )
        )
        filepath = self._get_xy_filepath(self.filepath)
        darray = self._get_xy_array(self.axis, data)
        np.savetxt(filepath, darray)


# default outputs
dofr = Outputter(AXISKEYS.R, "Å", "dofr", True)
gofr = Outputter(AXISKEYS.R, "Å", "gofr")
sofq = Outputter(AXISKEYS.Q, "Å⁻¹", "sofq", True)
sofq_inst = Outputter(AXISKEYS.Q_INST, "Å⁻¹", "sofq_inst")

default_outputs = [sofq_inst, sofq, gofr, dofr]
