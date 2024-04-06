import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import qt_interaction_handler
import light_ui

def main():
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = light_ui.Ui_MainWindow()
    ui.setupUi(MainWindow)

    qt_interaction_handler.setup_ui_interactions(ui)

    MainWindow.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()