import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets
import qt_handler
import light_ui
import procedure_handler
import extension_handler
from lights_global_state import LightsGlobalState

def main():
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = light_ui.Ui_MainWindow()
    ui.setupUi(MainWindow)

    glo = LightsGlobalState(app, ui, os.path.dirname(os.path.realpath(__file__)))

    extension_handler.setup_extensions(glo)
    procedure_handler.setup_procedures(glo)
    qt_handler.setup_ui(glo)

    if os.name == "nt":
        MainWindow.show()
    else:
        MainWindow.showFullScreen()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()