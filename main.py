import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTranslator, QLibraryInfo

from cad_window import CADWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)

    translator = QTranslator(app)
    if translator.load("qtbase_ru", QLibraryInfo.location(QLibraryInfo.TranslationsPath)):
        app.installTranslator(translator)

    wnd = CADWindow()

    sys.exit(app.exec_())

