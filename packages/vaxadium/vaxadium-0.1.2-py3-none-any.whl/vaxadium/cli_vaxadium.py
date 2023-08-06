"""Console script for vaxadium."""
import argparse
import sys

from vaxadium.logging_setup import add_logging_handlers
from vaxadium.runner import ExperimentRunner


def main():
    """Console script for vaxadium."""
    text = "collects a config and constructs the experiment runner"

    parser = argparse.ArgumentParser(description=text)
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        required=True,
        dest="output_fp",
        help="filepath to save data to",
    )
    parser.add_argument(
        "-c",
        "--config",
        type=str,
        required=True,
        dest="config_fp",
        help="filepath to config json file",
    )
    add_logging_handlers()
    args = parser.parse_args()

    runner = ExperimentRunner.from_json(args.config_fp)
    runner.set_output_file(args.output_fp)
    results = runner.run()
    results._write()
    results._close_nxs_file()
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
