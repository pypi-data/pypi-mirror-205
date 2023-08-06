import numpy as np

from vaxadium.checks import Checker


class ConvergenceChecker(Checker):
    def __init__(self):
        super().__init__()
        self.header = "Scaling Convergence Diagnostics"
        self.text = "The gain has converhed to a reasonable value"

    def _check(self, experiment):
        gain = experiment._gain
        delta = experiment._delta

        self.text = (
            "The gain has converged to a reasonable value (gain = {:.2e})".format(gain)
        )
        s = []
        s.append("----------------------------------------------------")
        s.append("Summary of the convergence")
        s.append("----------------------------------------------------")
        s.append("gain             : {:.2e}".format(gain))
        s.append("delta            : {:.3g}".format(delta))
        s.append("----------------------------------------------------")

        if any([np.isnan(x) for x in [gain, delta]]):
            self.level = 2
            self.text = "The gain diverged"
        elif abs(delta) > 1:
            self.level = 2
            self.text = "The gain did not converge (delta = {:.3g})".format(delta)
        elif abs(delta) > 1e-3:
            self.level = 1
            self.text = "The gain did not fully converge (delta = {:.3g})".format(delta)
        elif not 1e5 < gain < 1e14:
            self.level = 1
            self.text = (
                "The gain converged, but to an unusual value (gain = {:.2e})".format(
                    gain
                )
            )

        self._set_summary_from_list_of_lines(s)
