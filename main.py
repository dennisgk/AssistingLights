import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets
import qt_interaction_handler
import light_ui

os.environ["QT_ENABLE_HIGHDPI_SCALING"]   = "1"
os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
os.environ["QT_SCALE_FACTOR"]             = "1"

def main():
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = light_ui.Ui_MainWindow()
    ui.setupUi(MainWindow)

    qt_interaction_handler.setup_ui_interactions(app, ui)

    if os.name == "nt":
        MainWindow.show()
    else:
        MainWindow.showFullScreen()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()