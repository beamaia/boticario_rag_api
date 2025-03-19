import sys
import logging
import coloredlogs
import os

# add color to logs
coloredlogs.install(level='INFO')
log_file = "logs/log.txt"
logger = logging.getLogger(__name__)

# create console handler and set level to info
ch = logging.StreamHandler(sys.stdout)

if not os.path.exists("logs"):
    os.mkdir("logs")

fileh = logging.FileHandler(log_file)

# create formatter
formatter = logging.Formatter(
    "%(asctime)s %(levelname)s: %(message)s", "%Y-%m-%d %H:%M:%S"
)

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)
logger.addHandler(fileh)