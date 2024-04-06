import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets
import qt_interaction_handler
import light_ui

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