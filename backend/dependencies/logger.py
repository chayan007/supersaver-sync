import logging
import sys

logger = logging.getLogger('SuperSaverSync')
logger.propagate = False
# iteratively removing default lambda log handlers
for h in logger.handlers:
    logger.removeHandler(h)

# collecting the stream handler which is used for setting the new formats
h = logging.StreamHandler(sys.stdout)

FORMAT = '[%(levelname)s] %(message)s'
h.setFormatter(logging.Formatter(FORMAT))

# add the new handlers to the logger
logger.addHandler(h)

# we can run the logging on DEBUG to ensure that credentials are not printed if none then we can use INFO
logger.setLevel(logging.INFO)
