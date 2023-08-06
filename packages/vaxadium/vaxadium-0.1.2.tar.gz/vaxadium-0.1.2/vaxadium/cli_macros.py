"""Console script for vaxadium.macro"""
import argparse
import sys
from pathlib import Path

from vaxadium.constants import NEWNXXPDFNEXUSKEYS, NEWNXXPDFNEXUSKEYSARC
from vaxadium.g4diffsim.macro_maker import save_macro_file
from vaxadium.io.nexus_reader import NexusReaderSample
from vaxadium.io.serializer_factory import SERIALIZERS, nexus_serializer


def main():
    text = (
        "extract the relevant information from an nxxpdf nexus "
        "file and creates a mac file for g4diffsim"
    )

    parser = argparse.ArgumentParser(description=text)
    parser.add_argument(
        "-n",
        "--nxxpdf_nexus_file_path",
        type=str,
        required=True,
        dest="nxxpdf_fp",
        help="filepath to nxxpdf  nxs file",
    )
    parser.add_argument(
        "-o",
        "--output_file_path",
        type=str,
        required=True,
        dest="output_fp",
        help="Location to save the resulting macro file",
    )
    parser.add_argument(
        "-s",
        "--shape",
        type=str,
        required=False,
        dest="shape",
        choices=["flat", "cylinder"],
        help="The shape of the detector",
    )

    args = parser.parse_args()
    nxxpdf_fp = Path(args.nxxpdf_fp).absolute()
    output_fp = Path(args.output_fp).absolute()

    if args.shape == "cylinder":
        nxs = NexusReaderSample(NEWNXXPDFNEXUSKEYSARC)
    else:
        nxs = NexusReaderSample(NEWNXXPDFNEXUSKEYS)
    nxs.read(nxxpdf_fp, False)
    nxs.params["detector_shape"] = args.shape
    macros = nexus_serializer.serialize(nxs, SERIALIZERS.G4DIFFSIM)
    save_macro_file(macros, output_fp)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
