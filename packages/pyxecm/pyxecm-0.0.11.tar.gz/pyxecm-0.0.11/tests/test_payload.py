from pyxecm.payload import *


if __name__ == "__main__":

    # Configure logging output
    logging.basicConfig(
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
        datefmt="%d-%b-%Y %H:%M:%S",
        level=logging.DEBUG,
    )
    logger = logging.getLogger(os.path.basename(__file__))

    logger.info("Executing Payload test code...")

    payload_file = "/tmp/payload.yaml"

    payload_object = Payload(payload_file, "", None, None, None, None, None, None)
    if payload_object.initPayload():
        logger.error(
            "Failed to initialize payload -> {}".format(
                payload_file)
        )
        # Now process the payload in the defined ordering:
        # payload_object.processPayload()
        # users = payload_object.getUsers()