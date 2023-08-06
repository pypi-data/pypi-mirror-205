from pyxecm.otiv import *


if __name__ == "__main__":

    # some test code ...

    # Configure logging output
    logging.basicConfig(
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
        datefmt="%d-%b-%Y %H:%M:%S",
        level=logging.DEBUG,
    )
    logger = logging.getLogger(os.path.basename(__file__))

    logger.info("Executing OTIV test code...")

    otiv_object = OTIV("iv", "Viewing", "OpenText Intelligent Viewing", "/tmp/otiv-license.lic", "FULLTIME_USERS_REGULAR")

    # Retrieve configuration:
    config = otiv_object.config()
    logger.info(config)
