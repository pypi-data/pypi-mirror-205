import logging

import numpy as np
import scipy.optimize as opt
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression

from vaxadium.logging_setup import Capturing

logger = logging.getLogger(__name__)


def n_rotated_exponentials(tth_chi_r, bkg, power, *args):
    tth, chi, r = tth_chi_r
    x = r * np.cos(chi)
    y = r * np.sin(chi)
    chi_dependence = np.power(tth, power) * (
        np.sin(chi) + 1 * (r == 0)
    )  # forces middle pixel to be 1 rather than 0. this is ...
    arr = np.ones_like(x) * bkg  # important to avoid spurious fitting
    for i in range(len(args) // 3):
        a = args[3 * i] * np.exp(-(args[3 * i + 1] * x**2 + args[3 * i + 2] * y**2))
        if i == 0:
            arr += np.square(chi_dependence) * a
        else:
            arr += a
    return arr.ravel()


functions = {}
functions["standard"] = {
    "f": n_rotated_exponentials,
    "p0": [0.00005, 1.0]
    + [1e0, 10, 10] * 1
    + [1e-2, 1e3, 1e3] * 2
    + [1e-2, 1e2, 1e2] * 2,
    "bounds": (0, 1e6),
}
functions["standard_bounded"] = {
    "f": n_rotated_exponentials,
    "p0": [0.00005, 1.0]
    + [0.1, 10, 10] * 1
    + [1e-2, 1e3, 1e3] * 2
    + [1e-2, 1e2, 1e2] * 2,
    "bounds": (
        [0 for x in range(17)],
        [1, 5, 1, 1e4, 1e4, 1, 1e4, 1e4, 1, 1e4, 1e4, 1, 1e4, 1e4, 1, 1e4, 1e4],
    ),
}


class Extraction:
    def __init__(self, f, p0, bounds):
        logger.debug(
            "constructing Extraction object with function {}".format(f.__name__)
        )
        self.f = f
        self.p0 = p0
        self.bounds = bounds
        self.popt = []
        self.r_squared = None
        self.fitted_result = []

    @classmethod
    def from_library(cls, label="standard"):
        try:
            library_fucntion = functions[label]
        except KeyError:
            logger.error('function "{}" not found'.format(label))
            raise
        (f, p0, bounds) = (library_fucntion[a] for a in ["f", "p0", "bounds"])
        return cls(f, p0, bounds)

    def fit(self, tth_chi_r, data):
        logger.info("Fitting data...")
        self.data_shape = data.shape
        with Capturing() as output:
            popt, _ = opt.curve_fit(
                self.f,
                tth_chi_r,
                data.ravel(),
                p0=self.p0,
                bounds=self.bounds,
                verbose=2,
                xtol=1e-9,
            )
        logger.info(" ".join(output[-2:]))
        self.fitted_result = self.f(tth_chi_r, *popt).reshape(self.data_shape)
        ss_res = np.square(data - self.fitted_result).sum()
        mean_val = np.mean(data)
        ss_tot = np.square(data - mean_val).sum()
        self.r_squared = 1 - ss_res / ss_tot
        self.popt = popt

    def interpolate(self, tth_chi_r):
        return self.f(tth_chi_r, *self.popt)

    def __repr__(self):
        output = ("r_squared: {};  " "popt: {};  " "p0: {}.").format(
            self.r_squared, list(self.popt), self.p0
        )
        return output


class LinearRegressionExtraction:
    def __init__(self):
        logger.debug("constructing sklearn thing Extraction object ")
        self.regressor = LinearRegression()
        self.data_shape = None
        self.r_squared = 12
        self.fitted_result = []

    def fit(self, tth_chi_r, data):
        # just use tth and chi for the moment
        tth, chi, r = tth_chi_r
        input_array = np.asarray([x for x in zip(tth.ravel(), chi.ravel())])
        self.regressor.fit(input_array, data.ravel())

    def interpolate(self, tth_chi_r):
        tth, chi, r = tth_chi_r
        input_array = np.asarray([x for x in zip(tth.ravel(), chi.ravel())])
        return self.regressor.predict(input_array)


class RandomForestExtraction:
    def __init__(self):
        logger.debug("constructing sklearn random forest Extraction object ")
        self.regressor = RandomForestRegressor(n_estimators=1000, random_state=0)
        self.data_shape = None
        self.r_squared = 12
        self.fitted_result = []

    def fit(self, tth_chi_r, data):
        # just use tth and chi for the moment
        tth, chi, r = tth_chi_r
        input_array = np.asarray([x for x in zip(tth.ravel(), chi.ravel())])
        self.regressor.fit(input_array, data.ravel())

    def interpolate(self, tth_chi_r):
        tth, chi, r = tth_chi_r
        input_array = np.asarray([x for x in zip(tth.ravel(), chi.ravel())])
        return self.regressor.predict(input_array)
