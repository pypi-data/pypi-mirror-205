import logging
import sys
from io import StringIO
from pathlib import Path

import numpy as np

np.set_printoptions(threshold=20)

logger = logging.getLogger()


def add_logging_handlers(filename="vaxadium.log", stream_level=logging.INFO):
    path = Path(filename).expanduser().absolute()
    f_handler = logging.FileHandler(path, mode="w")
    f_handler.setLevel(logging.DEBUG)
    f_format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    f_handler.setFormatter(f_format)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(f_handler)
    logger.info("log file handler added")
    s_handler = logging.StreamHandler(sys.stdout)
    s_handler.setLevel(stream_level)
    s_format = logging.Formatter("%(name)s - %(levelname)s - %(message)s")
    s_handler.setFormatter(s_format)
    logger.addHandler(s_handler)


class Capturing(list):
    # https://stackoverflow.com/questions/16571150/how-to-capture-stdout-output-from-a-python-function-call
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self

    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio  # free up some memory
        sys.stdout = self._stdout
