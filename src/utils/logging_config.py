import logging

# Setup the basic logging configuration and date formatting
logging.basicConfig(
    format="%(asctime)s.%(msecs)03d %(levelname)s %(module)s:%(lineno)s %(message)s",
    datefmt="%d/%m/%Y %H:%M:%S",
)
# Limit the root logger to INFO
logger = logging.getLogger()

# Expose all INFO logs to CloudWatch
logger.setLevel(logging.INFO)

# Expose pynetdicom logs more verbosely
logging.getLogger("pynetdicom").setLevel(logging.DEBUG)
