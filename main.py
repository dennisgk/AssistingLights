import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets
import qt_handler
import light_ui
import procedure_handler
import extension_handler
from background_event_handler import stop_proc
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
    
    exitCode = app.exec_()

    proc_states_copy = [proc for proc in glo.proc_states]

    for proc_key in proc_states_copy:
        stop_proc(glo, proc_key)

    glo.quit_background_dispatch()

    sys.exit(exitCode)

if __name__ == "__main__":
    main()