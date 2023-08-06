"""
Created on 14 May 2019

@author: Timothy Spain, timothy.spain@diamond.ac.uk
"""
import logging
from abc import ABC, abstractmethod

import numpy as np

from vaxadium.configuration import AXISKEYS, CONFIGKEYS
from vaxadium.core.fourier import (
    FT_qtor,
    FT_qtor_Lorch,
    FT_rtoq,
    topHatConvolutionSubtraction,
)

logger = logging.getLogger(__name__)


class ScaledResultProcessor(ABC):
    def __init__(self, configuration={}):
        self.configuration = configuration

    @abstractmethod
    def call(self, scaled_result, configuration):
        pass

    def __call__(self, scaled_result):
        # Configure the configuration
        configuration = {**self.configuration, **scaled_result.configuration}
        # call the function
        c = {k: v for k, v in configuration.items() if k not in vars(AXISKEYS).values()}
        logger.debug("{} called with configuration {}".format(self.__class__, c))
        self.call(scaled_result, configuration)

    @property
    @abstractmethod
    def keys(self):
        pass

    @classmethod
    def from_collection(cls, collection):
        config = {k: collection.configuration[k] for k in cls.keys}
        return cls(config)


class TopHatter(ScaledResultProcessor):
    keys = [
        CONFIGKEYS.TOPHAT_WIDTH,
        CONFIGKEYS.RMAX,
        CONFIGKEYS.RSTEP,
        CONFIGKEYS.RMIN,
        CONFIGKEYS.RMINFT,
        CONFIGKEYS.QMAX,
        AXISKEYS.R,
        AXISKEYS.Q,
        AXISKEYS.Q_INST,
        AXISKEYS.ITRUNC,
    ]

    def call(self, scaled_result, config):
        q_width = config[CONFIGKEYS.TOPHAT_WIDTH]
        if config[CONFIGKEYS.RMINFT] == 0:
            error_text = "cannot have first bin centred at 0 for maths reasons"
            logger.error(error_text)
            raise ValueError(error_text)

        r = config[AXISKEYS.R]
        r_min = config[CONFIGKEYS.RMIN]
        rho = scaled_result.rho
        q_inst = config[AXISKEYS.Q_INST]

        f_tophat = topHatConvolutionSubtraction(q_inst, scaled_result.dscs, q_width)
        f_topped = scaled_result.dscs - f_tophat
        d_topped = FT_qtor(q_inst, f_topped, rho, r)

        fqt = (
            3
            * np.power(q_width * r, -3)
            * (np.sin(q_width * r) - q_width * r * np.cos(q_width * r))
        )
        br_topped = -d_topped * fqt / (1 - fqt)
        br_topped[r < r_min] = d_topped[r < r_min] + scaled_result.g0_minus_1
        bq_topped = FT_rtoq(r, br_topped, rho, q_inst)

        sofq_inst = f_topped - bq_topped

        i = config[AXISKEYS.ITRUNC]
        q = config[AXISKEYS.Q]
        sofq = sofq_inst[:i]

        scaled_result.q = q
        scaled_result.sofq_inst = sofq_inst
        scaled_result.sofq = sofq
        scaled_result.r = r


class FourierTransformer(ScaledResultProcessor):
    keys = [CONFIGKEYS.LORCH_WIDTH]

    def call(self, scaled_result, config):
        scaled_result.hofr = FT_qtor_Lorch(
            scaled_result.q,
            scaled_result.sofq,
            scaled_result.rho,
            scaled_result.r,
            config[CONFIGKEYS.LORCH_WIDTH],
        )

        scaled_result.gofr = scaled_result.hofr / scaled_result.g0_minus_1

        scaled_result.dofr = (
            scaled_result.gofr * scaled_result.r * 4 * np.pi * scaled_result.rho
        )
