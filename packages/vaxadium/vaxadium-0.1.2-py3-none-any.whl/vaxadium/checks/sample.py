from vaxadium.checks import Checker


class SampleChecker(Checker):
    def __init__(self):
        super().__init__()
        self.header = "Sample-based Diagnostics"
        self.text = "The sample appears to be sensible"

    def _check(self, experiment):
        # what do we need from the experiment?
        chemical_formula = experiment.sample.material
        mu = experiment.sample.mu
        r = experiment.sample.__r_outer__
        density = experiment.sample.density
        volume_fraction = experiment.sample.volume_fraction
        energy = experiment.dc.beam.energy
        mur = mu * r

        s = []
        s.append("----------------------------------------------------")
        s.append("Summary of this sample")
        s.append("----------------------------------------------------")
        s.append("Chemical Formula : {}".format(chemical_formula))
        s.append("Density          : {:7.3f} g/cm³".format(density))
        s.append("Packing Fraction : {:7.3f}".format(volume_fraction))
        s.append("Sample Radius    : {:7.3f} mm".format(r * 10))
        s.append("Beam Energy      : {:7.3f} keV".format(energy))
        s.append("µ                : {:7.3f} mm-1".format(mu / 10))
        s.append("µr               : {:7.3f}".format(mur))
        s.append("----------------------------------------------------")

        if mur > 3:
            self.level = 2
            self.text = "The sample is highly absorbing, µr = {}".format(mur)
        elif mur > 1:
            self.level = 1
            self.text = "The sample is rather absorbing, µr = {}".format(mur)

        self._set_summary_from_list_of_lines(s)
