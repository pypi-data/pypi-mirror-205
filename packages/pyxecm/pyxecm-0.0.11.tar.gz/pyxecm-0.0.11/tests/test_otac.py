from pyxecm.otac import *


if __name__ == "__main__":

    # some test code ...

    # Configure logging output
    logging.basicConfig(
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
        datefmt="%d-%b-%Y %H:%M:%S",
        level=logging.DEBUG,
    )
    logger = logging.getLogger(os.path.basename(__file__))

    logger.info("Executing OTAC test code...")

    endpoint = "otac.idea2sb.eimdemo.com"
    #    endpoint = "otpd.local.xecm.cloud"

    otac = OTAC("https", endpoint, 443, "dsadmin", "")

    response = otac.execCommand(
        "cf_create_host tmcelib1.eimdemo.biz 0 /archive 8080 8090"
    )

    response = otac.execCommand(
        "cf_set_variable MY_HOST_ALIASES otac-0,otac.idea2sb.eimdemo.com,otac DS"
    )

    print(response)
