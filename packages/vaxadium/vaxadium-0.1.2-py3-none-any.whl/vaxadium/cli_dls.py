"""Console script for vaxadium."""
import argparse
import logging
import sys
import traceback

from vaxadium.configuration import VaxadiumException
from vaxadium.logging_setup import add_logging_handlers
from vaxadium.runner import ExperimentRunner, get_config_from_file


def main():
    """Console script for vaxadium."""
    text = (
        "collects a config, a nxs, and a simulation (for the sample) "
        "and constructs the experiment runner"
    )

    parser = argparse.ArgumentParser(description=text)
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        required=True,
        dest="output",
        help="filepath to save data to",
    )
    parser.add_argument(
        "-c",
        "--config",
        type=str,
        required=True,
        dest="config",
        help="filepath to config json file",
    )
    parser.add_argument(
        "-n",
        "--nexus",
        type=str,
        required=True,
        dest="nxs",
        help="filepath to sample nxs files",
    )
    parser.add_argument(
        "-s",
        "--simulation",
        type=str,
        required=True,
        dest="sim",
        help="filepath to simulation nxs file",
    )
    parser.add_argument(
        "-d",
        "--diagnostics",
        type=str,
        required=False,
        dest="diagnostics",
        default=None,
        help="filepath to diagnostics file",
    )
    parser.add_argument(
        "-l", "--log", type=str, required=True, dest="log", help="path for a log file"
    )
    args = parser.parse_args()
    add_logging_handlers(args.log)
    config = get_config_from_file(args.config)
    # now append the other arguments into the config dict
    config["sample"] = {"dc": args.nxs, "sim": args.sim}
    try:
        runner = ExperimentRunner.from_configuration_dictionary(config)
        runner.set_output_file(args.output)
        runner.set_diagnostics_file(args.diagnostics)
        results = runner.run()
        runner.do_diagnostics_checks()
        results._write()
        results._close_nxs_file()
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
