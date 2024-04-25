from PyQt5.QtWidgets import QMessageBox, QColorDialog
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import Qt

def try_quit_application(glo):
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
        glo.app.quit()

def launch_color_dialog():
    color = QColorDialog.getColor()

# needed to do is in script auto implement moving the creation logic, translation logic, and adding procedure_rows
def generate_procedure_row(glo, proc):
    num_id = len(glo.ui.procedure_rows)

    procedure_sample_row = QtWidgets.QFrame(glo.ui.procedure_scroll_widgets)
    procedure_sample_row.setMinimumSize(QtCore.QSize(0, 80))
    procedure_sample_row.setMaximumSize(QtCore.QSize(16777215, 80))
    procedure_sample_row.setStyleSheet("")
    procedure_sample_row.setFrameShape(QtWidgets.QFrame.NoFrame)
    procedure_sample_row.setFrameShadow(QtWidgets.QFrame.Plain)
    procedure_sample_row.setLineWidth(1)
    procedure_sample_row.setObjectName(f"procedure_sample_row_{num_id}")
    verticalLayout_9 = QtWidgets.QVBoxLayout(procedure_sample_row)
    verticalLayout_9.setContentsMargins(0, 0, 0, 0)
    verticalLayout_9.setSpacing(0)
    verticalLayout_9.setObjectName(f"verticalLayout_9_{num_id}")
    procedure_sample_top_line = QtWidgets.QFrame(procedure_sample_row)
    procedure_sample_top_line.setFrameShadow(QtWidgets.QFrame.Plain)
    procedure_sample_top_line.setFrameShape(QtWidgets.QFrame.HLine)
    procedure_sample_top_line.setObjectName(f"procedure_sample_top_line_{num_id}")
    verticalLayout_9.addWidget(procedure_sample_top_line)
    procedure_sample_content = QtWidgets.QFrame(procedure_sample_row)
    procedure_sample_content.setFrameShape(QtWidgets.QFrame.NoFrame)
    procedure_sample_content.setFrameShadow(QtWidgets.QFrame.Raised)
    procedure_sample_content.setObjectName(f"procedure_sample_content_{num_id}")
    horizontalLayout_4 = QtWidgets.QHBoxLayout(procedure_sample_content)
    horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
    horizontalLayout_4.setSpacing(0)
    horizontalLayout_4.setObjectName(f"horizontalLayout_4_{num_id}")
    procedure_sample_left = QtWidgets.QFrame(procedure_sample_content)
    procedure_sample_left.setFrameShape(QtWidgets.QFrame.NoFrame)
    procedure_sample_left.setFrameShadow(QtWidgets.QFrame.Raised)
    procedure_sample_left.setObjectName(f"procedure_sample_left_{num_id}")
    verticalLayout_10 = QtWidgets.QVBoxLayout(procedure_sample_left)
    verticalLayout_10.setObjectName(f"verticalLayout_10_{num_id}")
    procedure_sample_title = QtWidgets.QLabel(procedure_sample_left)
    font = QtGui.QFont()
    font.setBold(True)
    procedure_sample_title.setFont(font)
    procedure_sample_title.setObjectName(f"procedure_sample_title_{num_id}")
    verticalLayout_10.addWidget(procedure_sample_title)
    procedure_sample_desc = QtWidgets.QLabel(procedure_sample_left)
    procedure_sample_desc.setObjectName(f"procedure_sample_desc_{num_id}")
    verticalLayout_10.addWidget(procedure_sample_desc)
    horizontalLayout_4.addWidget(procedure_sample_left)
    procedure_sample_button = QtWidgets.QPushButton(procedure_sample_content)
    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Ignored)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(procedure_sample_button.sizePolicy().hasHeightForWidth())
    procedure_sample_button.setSizePolicy(sizePolicy)
    procedure_sample_button.setMinimumSize(QtCore.QSize(70, 70))
    procedure_sample_button.setMaximumSize(QtCore.QSize(70, 70))
    procedure_sample_button.setStyleSheet("QPushButton {\n"
"    border: none;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: rgb(33, 37, 43);\n"
"}\n"
"QPushButton:pressed {    \n"
"    background-color: rgb(85, 170, 255);\n"
"}")
    procedure_sample_button.setText("")
    icon3 = QtGui.QIcon()
    icon3.addPixmap(QtGui.QPixmap(":/icons/filter.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    procedure_sample_button.setIcon(icon3)
    procedure_sample_button.setIconSize(QtCore.QSize(56, 56))
    procedure_sample_button.setObjectName(f"procedure_sample_button_{num_id}")
    horizontalLayout_4.addWidget(procedure_sample_button)
    verticalLayout_9.addWidget(procedure_sample_content)
    procedure_sample_bottom_line = QtWidgets.QFrame(procedure_sample_row)
    procedure_sample_bottom_line.setFrameShadow(QtWidgets.QFrame.Plain)
    procedure_sample_bottom_line.setLineWidth(1)
    procedure_sample_bottom_line.setFrameShape(QtWidgets.QFrame.HLine)
    procedure_sample_bottom_line.setObjectName(f"procedure_sample_bottom_line_{num_id}")
    verticalLayout_9.addWidget(procedure_sample_bottom_line)
    glo.ui.verticalLayout_8.addWidget(procedure_sample_row, 0, QtCore.Qt.AlignTop)

    _translate = QtCore.QCoreApplication.translate

    procedure_sample_title.setText(_translate("MainWindow", proc.name))
    procedure_sample_desc.setText(_translate("MainWindow", proc.desc))

    procedure_sample_button.clicked.connect(lambda: set_page_config(glo, proc))

    glo.ui.procedure_rows.append(procedure_sample_row)

def set_page_home(glo):
    glo.ui.main_display_stack.setCurrentIndex(0)

def set_page_action(glo):
    glo.ui.main_display_stack.setCurrentIndex(1)

def set_page_settings(glo):
    glo.ui.main_display_stack.setCurrentIndex(2)

def set_page_config(glo, proc):
    # now setup the config page before switching
    glo.ui.main_display_stack.setCurrentIndex(3)

def setup_ui(glo):
    glo.ui.home_button.clicked.connect(lambda: set_page_home(glo))
    glo.ui.action_button.clicked.connect(lambda: set_page_action(glo))
    glo.ui.settings_button.clicked.connect(lambda: set_page_settings(glo))

    glo.ui.verticalLayout_8.setAlignment(Qt.AlignTop)

    for proc in glo.procedures:
        glo.ui.procedure_rows.append(generate_procedure_row(glo, proc))

    glo.ui.exit_app_button.clicked.connect(lambda: try_quit_application(glo))

    set_page_home(glo)