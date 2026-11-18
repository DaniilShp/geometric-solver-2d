import logging
import os
import sys


def setup_logging():
    level_name = os.environ.get("CAD_LOG_LEVEL", "INFO").upper()
    level = getattr(logging, level_name, logging.INFO)

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(
        "%(asctime)s %(levelname)-8s %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    ))

    logging.basicConfig(level=level, handlers=[handler], force=True)
