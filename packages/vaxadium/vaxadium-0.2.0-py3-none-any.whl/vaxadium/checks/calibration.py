import numpy as np

from vaxadium.checks import Checker
from vaxadium.constants import PHYSICAL
from vaxadium.core.units import Q_


class CalibrationChecker(Checker):
    def __init__(self):
        super().__init__()
        self.header = "Detector Calibration Diagnostics"
        self.text = "The calibrations are all self-consistent"

    def _check(self, experiment):
        dc_energies_from_meta = [
            Q_(x.beam.energy, "keV").magnitude for x in experiment.all_data_collections
        ]
        dc_energies_from_pyfais = [
            PHYSICAL.SPEED_OF_LIGHT
            * PHYSICAL.PLANCK_CONSTANT
            / Q_(x.pyfai.wavelength, "m")
            for x in experiment.all_data_collections
        ]
        dc_energies_from_pyfais = [
            x.to("keV").magnitude for x in dc_energies_from_pyfais
        ]
        sim_energies_from_meta = [
            Q_(x.beam.energy, "keV").magnitude for x in experiment.simulations
        ]
        sim_energies_from_pyfais = [
            PHYSICAL.SPEED_OF_LIGHT
            * PHYSICAL.PLANCK_CONSTANT
            / Q_(x.pyfai.wavelength, "m")
            for x in experiment.simulations
        ]
        sim_energies_from_pyfais = [
            x.to("keV").magnitude for x in sim_energies_from_pyfais
        ]
        a = np.array(
            dc_energies_from_meta
            + dc_energies_from_pyfais
            + sim_energies_from_meta
            + sim_energies_from_pyfais
        )

        dc_names = [x.name for x in experiment.all_data_collections[1:]]

        fmtit = "{:15} | {:>9} | {:>9} | {:>9} | {:>9}"
        fmt = "{:15} | {:9.2f} | {:9.2f} | {:9.2f} | {:9.2f}"
        s = []
        s.append("---------------------------------------------------------------")
        s.append("Summary of the Primary Beam Energies")
        s.append("---------------------------------------------------------------")
        s.append(fmtit.format("", "dc_nexus", "dc_pyfai", "sim_nexus", "sim_pyfai"))
        s.append(
            fmt.format(
                "bkg",
                dc_energies_from_meta.pop(0),
                dc_energies_from_pyfais.pop(0),
                0,
                0,
            )
        )
        for name, ne, pe, sne, spe in zip(
            dc_names,
            dc_energies_from_meta,
            dc_energies_from_pyfais,
            sim_energies_from_meta,
            sim_energies_from_pyfais,
        ):
            s.append(fmt.format(name, ne, pe, sne, spe))
        s.append("---------------------------------------------------------------")

        max_difference = abs((a - a.mean())).max()
        if max_difference > 1:
            self.level = 2
            self.text = "There is a discrepancy with the incident beam energies"
        elif max_difference > 0.1:
            self.level = 1
            self.text = (
                "Some of the primary beam energies are potentially not exactly correct"
            )

        self._set_summary_from_list_of_lines(s)
