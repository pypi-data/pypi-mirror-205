from pyxecm.web import *


if __name__ == "__main__":

    # some test code ...

    # Configure logging output
    logging.basicConfig(
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
        datefmt="%d-%b-%Y %H:%M:%S",
        level=logging.DEBUG,
    )
    logger = logging.getLogger(os.path.basename(__file__))

    logger.info("Executing HTTP test code...")

    http_object = HTTP()

    response = http_object.httpRequest("https://www.heise.de", "GET")

    print(response)
