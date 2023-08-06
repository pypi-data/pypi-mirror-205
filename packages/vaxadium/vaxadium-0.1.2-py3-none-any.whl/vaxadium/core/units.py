from pint import UnitRegistry

ureg = UnitRegistry()

ureg.define("fraction = [] = frac")
ureg.define("percent = 1e-2 frac = %")
ureg.define("ppm = 1e-6 fraction")

Q_ = ureg.Quantity


def QA_(values, unit):
    # convert all values to unit of first
    u = values[0].units
    normalised_values = [v.to(u).magnitude for v in values]
    return Q_(normalised_values, u)
