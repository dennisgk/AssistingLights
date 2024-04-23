from PyQt5.QtWidgets import QMessageBox, QColorDialog
from PyQt5 import QtCore

from lights_global_state import LightsPage

def try_quit_application(app):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)

    msg.setWindowFlags(( QtCore.Qt.Window | QtCore.Qt.CustomizeWindowHint ) &~
        ( QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowSystemMenuHint | 
        QtCore.Qt.WindowMinimizeButtonHint | QtCore.Qt.WindowCloseButtonHint ))

    msg.setText("Are you sure you want to quit?")
    msg.setWindowTitle("Exit")

    msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    retVal = msg.exec_()

    if(retVal == QMessageBox.Yes):
        app.quit()

def launch_color_dialog():
    color = QColorDialog.getColor()

def setup_ui(glo):
    glo.ui.home_button.clicked.connect(lambda: glo.set_page(LightsPage.Home))
    glo.ui.action_button.clicked.connect(lambda: glo.set_page(LightsPage.Action))
    glo.ui.settings_button.clicked.connect(lambda: glo.set_page(LightsPage.Settings))
    glo.ui.procedure_sample_button.clicked.connect(lambda: glo.set_page(LightsPage.Config))

    glo.ui.exit_app_button.clicked.connect(lambda: try_quit_application(glo.app))