from vaxadium.checks.basechecker import Checker
from vaxadium.checks.calibration import CalibrationChecker
from vaxadium.checks.convergence import ConvergenceChecker
from vaxadium.checks.data import (
    AbsoluteIntensityChecker,
    DataOverlapChecker,
    DataSimilarityChecker,
    PercentageSignalChecker,
)
from vaxadium.checks.extractor import ExtractorChecker
from vaxadium.checks.sample import SampleChecker

__all__ = [
    "CalibrationChecker",
    "ConvergenceChecker",
    "AbsoluteIntensityChecker",
    "DataOverlapChecker",
    "DataSimilarityChecker",
    "PercentageSignalChecker",
    "ExtractorChecker",
    "SampleChecker",
]


def run_diagnostics_checks(experiment):
    return [x().check(experiment) for x in Checker.__subclasses__()]
