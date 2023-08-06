import numpy as np
from pyFAI import units as pyFAIunits

from vaxadium.checks import Checker


def _datacheck(experiment):
    # what do we need from the experiment?
    data = []
    for d in experiment.all_data_collections:
        data.append(
            d.pyfai.integrate1d(
                d._data["normalised_to_io"],
                1000,
                correctSolidAngle=False,
                unit=pyFAIunits.Q_A,
                polarization_factor=0.9,
                radial_range=[0, 40],
            )
        )
    data.append(data.pop(0))  # now it's sample, containers... background
    trap_integral = [np.trapz(x[1], x[0]) for x in data]  # the integral of the data
    difference_plots = [
        data[i][1] - data[i + 1][1] for i in range(len(data) - 1)
    ]  # the difference between them
    bkg_differences = [
        np.trapz(data[i][1] - data[-1][1], data[0][0]) for i in range(len(data) - 1)
    ]  # the difference the between the bkg them
    integral_diffs = [
        trap_integral[i] - trap_integral[i + 1] for i in range(len(data) - 1)
    ]  # the difference between them
    negative_diff_count = [
        (x < 0).sum() for x in difference_plots
    ]  # the number of negative differences
    m = np.array([d[1] for d in data]).T
    d = m.T @ m
    norm = (m * m).sum(0, keepdims=True) ** 0.5
    similarities = d / norm / norm.T
    np.fill_diagonal(similarities, 0)
    names = (
        ["sample"]
        + ["container{}".format(i) for i in range(len(data) - 2)]
        + ["background"]
    )
    s_all = []
    s = []
    template = "{:>12} : {:12.2f} {}"
    s.append("==========================================================")
    s.append(" Integrals of the data")
    s.append("----------------------------------------------------------")
    s.append("     dataset :     integral")
    for i, (n, ti) in enumerate(zip(names, trap_integral)):
        if i > 0:
            s.append(
                template.format(
                    n, ti, "({:.1f} difference)".format(integral_diffs[i - 1])
                )
            )
        else:
            s.append(template.format(n, ti, ""))

    s.append("----------------------------------------------------------")
    s.append(" Methodology")
    s.append(" Integrals are calculated using numpy.trapz.")
    s_all.append(s)
    s = []
    s.append("==========================================================")
    s.append(" Negative intensities")
    s.append("----------------------------------------------------------")
    template = "{:>25} : {:5d}"
    s.append("               difference : number of negative intensities")
    for i, n in enumerate(negative_diff_count):
        s.append(template.format("{} - {}".format(names[i], names[i + 1]), n))
    s.append("----------------------------------------------------------")
    s.append(" Methodology")
    s.append(" Negative intensities are calculated as the number of histogram (Q)")
    s.append("  bins in which there is a negative residual when subtracting the outer")
    s.append("  dataset. For a typical powder in a capillary with a background")
    s.append("  scenario, we simply subtract the capillary from the sample and")
    s.append("  the background from the capillary")
    s_all.append(s)
    s = []
    s.append("==========================================================")
    s.append(" Background differences")
    s.append("----------------------------------------------------------")
    s.append("{} ".format(bkg_differences))
    s_all.append(s)
    s.append("----------------------------------------------------------")
    s.append(" Methodology")
    s.append(" Background difference is the np.trapz difference between each of the")
    s.append("  non-background datasets and the background data.")
    s = []
    s.append("==========================================================")
    s.append(" Similarity of data")
    s.append("----------------------------------------------------------")
    template = "{:>10} " + "{:10.5f} " * len(names)
    ttemplate = "{:>10} " * (len(names) + 1)
    s.append(ttemplate.format(*([""] + names)))
    for i in range(len(names)):
        s.append(template.format(*([names[i]] + list(similarities[i]))))
    s.append("----------------------------------------------------------")
    s.append(" Methodology")
    s.append(" Similarities use a cosine distance.")
    s_all.append(s)
    output = {
        "string": s_all,
        "trap_integral": trap_integral,
        "integral_diffs": integral_diffs,
        "negative_diff_count": negative_diff_count,
        "similarities": similarities,
        "bkg_differences": bkg_differences,
    }

    return output


class AbsoluteIntensityChecker(Checker):
    def __init__(self):
        super().__init__()
        self.header = "Absolute Intensity Checks"
        self.text = "The absolute intensities of the data are non-zero"

    def _check(self, experiment):
        checkdata = _datacheck(experiment)
        trap_integral = checkdata["trap_integral"]
        if any([x < 50 for x in trap_integral]):
            self.level = 2
            self.text = "One or more of the data have almost no counts"
        elif any([x < 1000 for x in trap_integral]):
            self.level = 1
            self.text = "One or more of the data have very few counts"
        self._set_summary_from_list_of_lines(checkdata["string"][0])


class DataSimilarityChecker(Checker):
    def __init__(self):
        super().__init__()
        self.header = "Data Similarity Checks"
        self.text = "The data look suitably different from one another"

    def _check(self, experiment):
        checkdata = _datacheck(experiment)
        if any([abs(x) < 1000 for x in checkdata["bkg_differences"]]):
            self.level = 2
            self.text = "One or more datasets _closely_ resembles the empty beamline"
        elif (checkdata["similarities"] > 0.997).any():
            self.level = 2
            self.text = (
                "One or more of the data have very high cosine similarity (>0.997)"
            )
        elif (checkdata["similarities"] > 0.99).any():
            self.level = 1
            self.text = "One or more of the data have high cosine similarity (>0.99)"
        self._set_summary_from_list_of_lines(
            checkdata["string"][2] + checkdata["string"][3]
        )


class DataOverlapChecker(Checker):
    def __init__(self):
        super().__init__()
        self.header = "Data Overlap Checks"
        self.text = "The data do not particularly overlap"

    def _check(self, experiment):
        checkdata = _datacheck(experiment)
        negative_diff_count = checkdata["negative_diff_count"]
        if any([x > 100 for x in negative_diff_count]):
            self.level = 2
            self.text = "One or more of the data are significantly overlapping"
        elif any([x > 30 for x in negative_diff_count]):
            self.level = 1
            self.text = "One or more of the data are somewhat overlapping"
        self._set_summary_from_list_of_lines(checkdata["string"][1])


class PercentageSignalChecker(Checker):
    def __init__(self):
        super().__init__()
        self.header = "Percentage Signal Checks"
        self.text = "A significant proportion of the sample signal is from the sample"

    def _check(self, experiment):
        checkdata = _datacheck(experiment)
        trap_integral = checkdata["trap_integral"]
        if len(trap_integral) < 2:
            self.text = "Test void. There are not enough datasets"
        else:
            percentage = 100 * (trap_integral[0] - trap_integral[1]) / trap_integral[0]
            if percentage < 5:
                self.level = 2
                self.text = (
                    "A significant proportion"
                    "({:.1f}%) of the sample signal is not from the sample".format(
                        100 - percentage
                    )
                )
            elif percentage < 15:
                self.level = 1
                self.text = (
                    "A large proportion "
                    "({:.1f}%) of the sample signal is not from the sample".format(
                        100 - percentage
                    )
                )
        self._set_summary_from_list_of_lines(checkdata["string"][0])
