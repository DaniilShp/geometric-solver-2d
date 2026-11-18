import logging
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTranslator, QLibraryInfo

from cad_window import CADWindow
from log_config import setup_logging

if __name__ == '__main__':
    setup_logging()
    logger = logging.getLogger("app")
    logger.info("Geometric solver started")

    app = QApplication(sys.argv)

    translator = QTranslator(app)
    if translator.load("qtbase_ru", QLibraryInfo.location(QLibraryInfo.TranslationsPath)):
        app.installTranslator(translator)
    else:
        logger.debug("Russian Qt translation not loaded")

    wnd = CADWindow()

    exit_code = app.exec_()
    logger.info("Geometric solver stopped")
    sys.exit(exit_code)

