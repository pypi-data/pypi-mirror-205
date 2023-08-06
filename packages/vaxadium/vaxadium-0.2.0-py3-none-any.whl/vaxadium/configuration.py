import numpy as np


class CKEYS:
    """The keys in the config json fed into vaxadium by the user/gda"""

    BACKGROUND = "background"
    SAMPLE = "sample"
    SIMULATION = "sim"
    DATACOLLECTION = "dc"
    CONTAINERn = "container{}"
    USER_CONFIG = "configuration"


class CONFIGKEYS:
    """The keys within the aforementioned configuration block in the json"""

    QMAX_INST = "qmax_inst"
    RMIN = "rmin"
    QSTEP = "qstep"
    QMIN = "qmin"
    QMAX = "qmax"
    GAIN = "gain"
    GAIN_RESULT = "gain_result"
    ITERATIONS = "iterations"
    POLARIZATION = "polarization"
    LORCH_WIDTH = "lorch_width"
    TOPHAT_WIDTH = "tophat_width"
    RMINFT = "rmin_ft"
    RMAX = "rmax"
    RSTEP = "rstep"
    FSQUARED = "form_factor_normalisation"


class FORMFACTORKEYS:
    SUMOFSQUARES = "sum_of_squares"
    SQUAREOFSUMS = "square_of_sums"


class AXISKEYS:
    Q = "q"
    R = "r"
    Q_INST = "q_inst"
    ITRUNC = "itrunc"


class VaxadiumException(Exception):
    pass


class UnrecognisedKeyException(VaxadiumException):
    pass


class VaxadiumConfigurationError(VaxadiumException):
    pass


class LockedDict(dict):
    def __setitem__(self, key, value):
        if key not in self:
            raise UnrecognisedKeyException(
                "{} is not a legal key of this Dict".format(repr(key))
            )
        dict.__setitem__(self, key, value)


class DontPrintEverythingDict(dict):
    def __init__(self, *args, **kwargs):
        self.types_to_not_repr = []
        dict.__init__(self, *args, **kwargs)

    def __repr__(self):
        if self.keys():
            lines = []
            for key, value in self.items():
                if type(value) not in self.types_to_not_repr:
                    lines.append("'{}':{}".format(key, value))
                    print(lines)
                else:
                    lines.append("'{}': {}".format(key, type(value)))
            return "{ " + ", ".join(lines) + " }"
        else:
            return self.__class__.__name__ + "()"


MAX_NXS_SHAPE = 100

defaultconfig = DontPrintEverythingDict()
defaultconfig.types_to_not_repr.append(np.ndarray)
defaultconfig[CONFIGKEYS.QMAX_INST] = 32
defaultconfig[CONFIGKEYS.QMAX] = 27.5
defaultconfig[CONFIGKEYS.QSTEP] = 0.02
defaultconfig[CONFIGKEYS.QMIN] = 0.0
defaultconfig[CONFIGKEYS.RMIN] = 1.0
defaultconfig[CONFIGKEYS.GAIN] = 1.0
defaultconfig[CONFIGKEYS.GAIN_RESULT] = None
defaultconfig[CONFIGKEYS.ITERATIONS] = 10
defaultconfig[CONFIGKEYS.POLARIZATION] = 0.9
defaultconfig[CONFIGKEYS.LORCH_WIDTH] = 0.001
defaultconfig[CONFIGKEYS.TOPHAT_WIDTH] = 4
defaultconfig[CONFIGKEYS.RMINFT] = 0.025
defaultconfig[CONFIGKEYS.RMAX] = 25
defaultconfig[CONFIGKEYS.RSTEP] = 0.025
defaultconfig[CONFIGKEYS.FSQUARED] = FORMFACTORKEYS.SUMOFSQUARES
