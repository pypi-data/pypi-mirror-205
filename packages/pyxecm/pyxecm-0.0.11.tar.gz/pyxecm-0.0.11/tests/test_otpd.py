from pyxecm.otpd import *

if __name__ == "__main__":

    # some test code ...

    # Configure logging output
    logging.basicConfig(
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
        datefmt="%d-%b-%Y %H:%M:%S",
        level=logging.DEBUG,
    )
    logger = logging.getLogger(os.path.basename(__file__))

    logger.info("Executing OTPD test code...")

    endpoint = "otpd.dev.terrarium.xecm.dev"
    #    endpoint = "otpd.local.xecm.cloud"

    otpd = OTPD("https", endpoint, 443, "powerdocsapiuser", "Opentext1!")

    #    response = otpd.authenticate()

    response = otpd.applySetting("LocalOtdsUrl", "http://otds/otdsws")
    response = otpd.applySetting(
        "LocalApplicationServerUrlForContentManager",
        "http://localhost:8080/c4ApplicationServer",
        "Successfactors",
    )

    # response = otpddbimport.importDatabase(
    #     filename="/home/kgatzweiler/git/terraform/tf-python/src/dbexport.zip"
    # )
    # logger.info("Response -> {}".format(response))
