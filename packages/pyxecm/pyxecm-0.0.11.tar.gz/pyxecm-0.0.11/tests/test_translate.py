from pyxecm.translate import *


if __name__ == "__main__":

    # some test code ...

    # Configure logging output
    logging.basicConfig(
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
        datefmt="%d-%b-%Y %H:%M:%S",
        level=logging.DEBUG,
    )
    logger = logging.getLogger(os.path.basename(__file__))

    logger.info("Executing Google Translate test code...")

    google_translate = Translator(api_key="AIzaSyD9I5qEcuqMakYcOBKSOdCUpMtxKNahhP4", project_key="846626430249")
    translated_text_v2 = google_translate.translate(source_language="en", target_language="es", text="Hello, world!")
    logger.info(translated_text_v2)  # Hola mundo!

    translated_text_v3 = google_translate.translateV3(source_language="en", target_language="es", text="Hello, world!")
    logger.info(translated_text_v3)  # Hola mundo!
