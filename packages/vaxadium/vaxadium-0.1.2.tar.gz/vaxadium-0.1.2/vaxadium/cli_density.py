"""Console script for vaxadium."""
import argparse
import logging
import sys
import traceback

from vaxadium.configuration import VaxadiumException
from vaxadium.physics import atom_number_density


def main():
    """Console script for converting g / cm3 to atoms / cubic A."""
    text = "convert a chemical formula and a density to an atomic number density"

    parser = argparse.ArgumentParser(description=text)
    parser.add_argument(
        "-f",
        "--formula",
        type=str,
        required=True,
        dest="formula",
        help="chemical formula",
    )
    parser.add_argument(
        "-d",
        "--density",
        type=float,
        required=True,
        dest="density",
        help="density of material in g / cm3",
    )
    args = parser.parse_args()

    try:
        print(atom_number_density(args.formula, args.density) / 1e30)
    except VaxadiumException as e:
        template = "A {0} occurred:\n{1!r}"
        msg = template.format(type(e).__name__, e.args[0])
        logging.error(msg)
        return 1
    except Exception as e:
        template = "A {0} occurred:\n{1!r}"
        msg = template.format(type(e).__name__, e.args)
        logging.error(traceback.format_exc())
        logging.error(e)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
