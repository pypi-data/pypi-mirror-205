from vaxadium.checks import Checker


class ExtractorChecker(Checker):
    def __init__(self):
        super().__init__()
        self.header = "Simulation Extraction Diagnostics"
        self.text = "The fit to the simulation is good"

    def _check(self, experiment):
        ex = experiment.extractor
        name = ex.f.__name__
        r_squared = ex.r_squared
        popt = ex.popt

        self.text = "The fit to the simulation is good (r² = {:.3f})".format(r_squared)
        s = []
        s.append("----------------------------------------------------")
        s.append("Summary of the extraction")
        s.append("----------------------------------------------------")
        s.append("r²               : {}".format(r_squared))
        s.append("Function         : {}".format(name))
        s.append("popt  0          : {}".format(popt[0]))
        s.append("popt  1          : {}".format(popt[1]))
        s.append("popt  2:4        : {}".format(popt[2:5]))
        s.append("popt  5:7        : {}".format(popt[5:8]))
        s.append("popt  8:10       : {}".format(popt[8:11]))
        s.append("popt 11:13       : {}".format(popt[11:14]))
        s.append("popt 14:17       : {}".format(popt[14:]))
        s.append("----------------------------------------------------")

        if r_squared < 0.85:
            self.level = 2
            self.text = "The extractor fit is very poor (r² = {:.3f})".format(r_squared)
        elif r_squared < 0.92:
            self.level = 1
            self.text = "The extractor fit is not optimal (r² = {:.3f})".format(
                r_squared
            )
        self._set_summary_from_list_of_lines(s)
