from PyQt5.QtWidgets import QMessageBox, QColorDialog
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel
from procedure_handler import LightsProcedureColorArg, LightsProcedureSelectArg

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

def launch_color_dialog(color_def_callback, color_callback):
    color = QColorDialog.getColor(color_def_callback())
    color_callback(color)

def generate_procedure_desc(proc):
    return f"{", ".join(proc.domains)}\n{proc.desc}"

def generate_procedure_row(glo, proc):
    num_id = len(glo.ui.procedure_rows)

    procedure_sample_row = QtWidgets.QFrame(glo.ui.procedure_scroll_widgets)
    procedure_sample_row.setMinimumSize(QtCore.QSize(0, 80))
    procedure_sample_row.setMaximumSize(QtCore.QSize(16777215, 16777215))
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
    horizontalLayout_4.setContentsMargins(0, 0, 9, 0)
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
    procedure_sample_desc.setWordWrap(True)
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

    set_widget_text(procedure_sample_title, proc.name)
    set_widget_text(procedure_sample_desc, generate_procedure_desc(proc))

    procedure_sample_button.clicked.connect(lambda: set_page_config(glo, proc))

    return procedure_sample_row

def set_page_home(glo):
    remove_config_arg_rows_if_nec(glo)
    glo.ui.main_display_stack.setCurrentIndex(0)

def set_page_action(glo):
    remove_config_arg_rows_if_nec(glo)
    glo.ui.main_display_stack.setCurrentIndex(1)

def set_page_settings(glo):
    remove_config_arg_rows_if_nec(glo)
    glo.ui.main_display_stack.setCurrentIndex(2)

def generate_color_arg_row(glo, arg):
    num_id = len(glo.ui.config_arg_rows)

    args_color_sample_row = QtWidgets.QFrame(glo.ui.args_scroll_area)
    args_color_sample_row.setMinimumSize(QtCore.QSize(0, 80))
    args_color_sample_row.setMaximumSize(QtCore.QSize(16777215, 80))
    args_color_sample_row.setFrameShape(QtWidgets.QFrame.NoFrame)
    args_color_sample_row.setFrameShadow(QtWidgets.QFrame.Raised)
    args_color_sample_row.setObjectName(f"args_color_sample_row_{num_id}")
    verticalLayout_15 = QtWidgets.QVBoxLayout(args_color_sample_row)
    verticalLayout_15.setContentsMargins(0, 0, 0, 0)
    verticalLayout_15.setSpacing(0)
    verticalLayout_15.setObjectName(f"verticalLayout_15_{num_id}")
    args_color_sample_bottom_line = QtWidgets.QFrame(args_color_sample_row)
    args_color_sample_bottom_line.setFrameShadow(QtWidgets.QFrame.Plain)
    args_color_sample_bottom_line.setFrameShape(QtWidgets.QFrame.HLine)
    args_color_sample_bottom_line.setObjectName(f"args_color_sample_bottom_line_{num_id}")
    verticalLayout_15.addWidget(args_color_sample_bottom_line)
    args_color_main_frame = QtWidgets.QFrame(args_color_sample_row)
    args_color_main_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
    args_color_main_frame.setFrameShadow(QtWidgets.QFrame.Raised)
    args_color_main_frame.setObjectName(f"args_color_main_frame_{num_id}")
    horizontalLayout_7 = QtWidgets.QHBoxLayout(args_color_main_frame)
    horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
    horizontalLayout_7.setSpacing(0)
    horizontalLayout_7.setObjectName(f"horizontalLayout_7_{num_id}")
    args_color_left_frame = QtWidgets.QFrame(args_color_main_frame)
    args_color_left_frame.setFrameShape(QtWidgets.QFrame.NoFrame)
    args_color_left_frame.setFrameShadow(QtWidgets.QFrame.Raised)
    args_color_left_frame.setLineWidth(0)
    args_color_left_frame.setObjectName(f"args_color_left_frame_{num_id}")
    verticalLayout_17 = QtWidgets.QVBoxLayout(args_color_left_frame)
    verticalLayout_17.setObjectName(f"verticalLayout_17_{num_id}")
    args_color_title = QtWidgets.QLabel(args_color_left_frame)
    font = QtGui.QFont()
    font.setBold(True)
    font.setWeight(75)
    args_color_title.setFont(font)
    args_color_title.setObjectName(f"args_color_title_{num_id}")
    verticalLayout_17.addWidget(args_color_title)
    args_color_desc = QtWidgets.QLabel(args_color_left_frame)
    args_color_desc.setLineWidth(0)
    args_color_desc.setObjectName(f"args_color_desc_{num_id}")
    verticalLayout_17.addWidget(args_color_desc)
    horizontalLayout_7.addWidget(args_color_left_frame)
    args_color_right_frame = QtWidgets.QFrame(args_color_main_frame)
    args_color_right_frame.setMaximumSize(QtCore.QSize(300, 16777215))
    args_color_right_frame.setFrameShape(QtWidgets.QFrame.NoFrame)
    args_color_right_frame.setFrameShadow(QtWidgets.QFrame.Raised)
    args_color_right_frame.setLineWidth(0)
    args_color_right_frame.setObjectName(f"args_color_right_frame_{num_id}")
    verticalLayout_18 = QtWidgets.QVBoxLayout(args_color_right_frame)
    verticalLayout_18.setObjectName(f"verticalLayout_18_{num_id}")
    args_color_button = QtWidgets.QPushButton(args_color_right_frame)
    args_color_button.setMinimumSize(QtCore.QSize(0, 30))
    args_color_button.setStyleSheet("QPushButton {\n"
"    border: none;\n"
"    background-color: rgb(27, 29, 35);\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: rgb(33, 37, 43);\n"
"}\n"
"QPushButton:pressed {    \n"
"    background-color: rgb(85, 170, 255);\n"
"}")
    args_color_button.setObjectName(f"args_color_button_{num_id}")
    verticalLayout_18.addWidget(args_color_button)
    args_color_preview = QtWidgets.QLabel(args_color_right_frame)
    args_color_preview.setObjectName(f"args_color_preview_{num_id}")
    verticalLayout_18.addWidget(args_color_preview)
    horizontalLayout_7.addWidget(args_color_right_frame)
    verticalLayout_15.addWidget(args_color_main_frame)
    args_color_sample_top_line = QtWidgets.QFrame(args_color_sample_row)
    args_color_sample_top_line.setFrameShadow(QtWidgets.QFrame.Plain)
    args_color_sample_top_line.setFrameShape(QtWidgets.QFrame.HLine)
    args_color_sample_top_line.setObjectName(f"args_color_sample_top_line_{num_id}")
    verticalLayout_15.addWidget(args_color_sample_top_line)
    glo.ui.verticalLayout_14.addWidget(args_color_sample_row, 0, QtCore.Qt.AlignTop)

    set_widget_text(args_color_title, arg.name)
    set_widget_text(args_color_desc, arg.desc)
    set_widget_text(args_color_button, "Select Color")
    set_widget_text(args_color_preview, f"rgb({arg.color_def.red()}, {arg.color_def.green()}, {arg.color_def.blue()})")

    def color_callback(color):
        glo.config_arg_passed[arg.name] = color
        set_widget_text(args_color_preview, f"rgb({glo.config_arg_passed[arg.name].red()}, {glo.config_arg_passed[arg.name].green()}, {glo.config_arg_passed[arg.name].blue()})")

    def color_def_callback():
        return glo.config_arg_passed[arg.name]

    args_color_button.clicked.connect(lambda: launch_color_dialog(color_def_callback, color_callback))

    return args_color_sample_row

def generate_select_arg_row(glo, arg):
    num_id = len(glo.ui.config_arg_rows)

    args_select_sample_row = QtWidgets.QFrame(glo.ui.args_scroll_area)
    args_select_sample_row.setMinimumSize(QtCore.QSize(0, 80))
    args_select_sample_row.setMaximumSize(QtCore.QSize(16777215, 80))
    args_select_sample_row.setFrameShape(QtWidgets.QFrame.NoFrame)
    args_select_sample_row.setFrameShadow(QtWidgets.QFrame.Raised)
    args_select_sample_row.setLineWidth(0)
    args_select_sample_row.setObjectName(f"args_select_sample_row_{num_id}")
    verticalLayout_19 = QtWidgets.QVBoxLayout(args_select_sample_row)
    verticalLayout_19.setContentsMargins(0, 0, 0, 0)
    verticalLayout_19.setSpacing(0)
    verticalLayout_19.setObjectName(f"verticalLayout_19_{num_id}")
    args_select_sample_top_line = QtWidgets.QFrame(args_select_sample_row)
    args_select_sample_top_line.setFrameShadow(QtWidgets.QFrame.Plain)
    args_select_sample_top_line.setFrameShape(QtWidgets.QFrame.HLine)
    args_select_sample_top_line.setObjectName(f"args_select_sample_top_line_{num_id}")
    verticalLayout_19.addWidget(args_select_sample_top_line)
    args_select_main_frame = QtWidgets.QFrame(args_select_sample_row)
    args_select_main_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
    args_select_main_frame.setFrameShadow(QtWidgets.QFrame.Raised)
    args_select_main_frame.setObjectName(f"args_select_main_frame_{num_id}")
    horizontalLayout_8 = QtWidgets.QHBoxLayout(args_select_main_frame)
    horizontalLayout_8.setContentsMargins(0, 0, 0, 0)
    horizontalLayout_8.setSpacing(0)
    horizontalLayout_8.setObjectName(f"horizontalLayout_8_{num_id}")
    args_select_left_frame = QtWidgets.QFrame(args_select_main_frame)
    args_select_left_frame.setFrameShape(QtWidgets.QFrame.NoFrame)
    args_select_left_frame.setFrameShadow(QtWidgets.QFrame.Raised)
    args_select_left_frame.setObjectName(f"args_select_left_frame_{num_id}")
    verticalLayout_20 = QtWidgets.QVBoxLayout(args_select_left_frame)
    verticalLayout_20.setObjectName(f"verticalLayout_20_{num_id}")
    args_select_title = QtWidgets.QLabel(args_select_left_frame)
    font = QtGui.QFont()
    font.setBold(True)
    font.setWeight(75)
    args_select_title.setFont(font)
    args_select_title.setObjectName(f"args_select_title_{num_id}")
    verticalLayout_20.addWidget(args_select_title)
    args_select_desc = QtWidgets.QLabel(args_select_left_frame)
    args_select_desc.setObjectName(f"args_select_desc_{num_id}")
    verticalLayout_20.addWidget(args_select_desc)
    horizontalLayout_8.addWidget(args_select_left_frame)
    args_select_right_frame = QtWidgets.QFrame(args_select_main_frame)
    args_select_right_frame.setMaximumSize(QtCore.QSize(300, 16777215))
    args_select_right_frame.setFrameShape(QtWidgets.QFrame.NoFrame)
    args_select_right_frame.setFrameShadow(QtWidgets.QFrame.Raised)
    args_select_right_frame.setObjectName(f"args_select_right_frame_{num_id}")
    verticalLayout_21 = QtWidgets.QVBoxLayout(args_select_right_frame)
    verticalLayout_21.setObjectName(f"verticalLayout_21_{num_id}")
    args_select_box = QtWidgets.QComboBox(args_select_right_frame)
    args_select_box.setCurrentText("")
    args_select_box.setObjectName(f"args_select_box_{num_id}")
    verticalLayout_21.addWidget(args_select_box)
    horizontalLayout_8.addWidget(args_select_right_frame)
    verticalLayout_19.addWidget(args_select_main_frame)
    args_select_sample_bottom_line = QtWidgets.QFrame(args_select_sample_row)
    args_select_sample_bottom_line.setFrameShadow(QtWidgets.QFrame.Plain)
    args_select_sample_bottom_line.setFrameShape(QtWidgets.QFrame.HLine)
    args_select_sample_bottom_line.setObjectName(f"args_select_sample_bottom_line_{num_id}")
    verticalLayout_19.addWidget(args_select_sample_bottom_line)
    glo.ui.verticalLayout_14.addWidget(args_select_sample_row)

    set_widget_text(args_select_title, arg.name)
    set_widget_text(args_select_desc, arg.desc)

    for option in arg.select_options:
        args_select_box.addItem(option)

    selected_index = 0
    for x in range(0, len(arg.select_options)):
        if(arg.select_options[x] == arg.select_def):
            selected_index = x
            break

    args_select_box.setCurrentIndex(selected_index)

    def on_current_index_changed(value):
        glo.config_arg_passed[arg.name] = arg.select_options[value]

    args_select_box.currentIndexChanged.connect(on_current_index_changed)

    return args_select_sample_row

def remove_config_arg_rows_if_nec(glo):
    if(glo.ui.main_display_stack.currentIndex() != 3):
        return
    
    glo.config_arg_passed = None
    glo.config_proc = None
    
    for arg in glo.ui.config_arg_rows:
        glo.ui.verticalLayout_14.removeWidget(arg)

def generate_simple_wrap_label(text):
    label = QLabel()
    label.setWordWrap(True)
    set_widget_text(label, text)

    return label

def set_widget_text(widget, text):
    _translate = QtCore.QCoreApplication.translate

    widget.setText(_translate("MainWindow", text))

def set_page_config(glo, proc):

    set_widget_text(glo.ui.run_page_title, proc.name)
    set_widget_text(glo.ui.run_page_desc, generate_procedure_desc(proc))

    temp_arg_passed = {}

    for arg in proc.args:
        if isinstance(arg, LightsProcedureColorArg):
            glo.ui.config_arg_rows.append(generate_color_arg_row(glo, arg))
            temp_arg_passed[arg.name] = arg.color_def

        if isinstance(arg, LightsProcedureSelectArg):
            glo.ui.config_arg_rows.append(generate_select_arg_row(glo, arg))
            temp_arg_passed[arg.name] = arg.select_def

    glo.config_arg_passed = temp_arg_passed
    glo.config_proc = proc

    glo.ui.main_display_stack.setCurrentIndex(3)

def on_click_run_proc(glo):
    glo.run_procedure(glo.config_proc, glo.config_arg_passed)

    set_page_home(glo)

def clear_output(glo):
    glo.ui.output_text_edit.setHtml("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>")

def setup_ui(glo):
    glo.ui.home_button.clicked.connect(lambda: set_page_home(glo))
    glo.ui.action_button.clicked.connect(lambda: set_page_action(glo))
    glo.ui.settings_button.clicked.connect(lambda: set_page_settings(glo))

    glo.ui.verticalLayout_14.setAlignment(Qt.AlignTop)
    glo.ui.verticalLayout_8.setAlignment(Qt.AlignTop)

    for proc in glo.procedures:
        glo.ui.procedure_rows.append(generate_procedure_row(glo, proc))

    glo.ui.exit_app_button.clicked.connect(lambda: try_quit_application(glo))
    glo.ui.run_procedure_start_button.clicked.connect(lambda: on_click_run_proc(glo))

    clear_output(glo)
    glo.ui.output_clear_button.clicked.connect(lambda: clear_output(glo))

    set_page_home(glo)