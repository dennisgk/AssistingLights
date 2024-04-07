from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtCore

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

def setup_ui_interactions(app, ui):
    ui.home_button.clicked.connect(lambda: ui.main_display_stack.setCurrentIndex(0))
    ui.action_button.clicked.connect(lambda: ui.main_display_stack.setCurrentIndex(1))
    ui.settings_button.clicked.connect(lambda: ui.main_display_stack.setCurrentIndex(2))

    ui.exit_app_button.clicked.connect(lambda: try_quit_application(app))