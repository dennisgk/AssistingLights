import sys
from PyQt5.QtWidgets import QApplication, QWidget

def main():
    app = QApplication(sys.argv)
    w = QWidget()
    w.resize(1024, 600)
    w.setWindowTitle("OX Spring 24 Project Software")
    w.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

"""
ui.home_button.clicked.connect(lambda: ui.main_display_stack.setCurrentIndex(0))
ui.action_button.clicked.connect(lambda: ui.main_display_stack.setCurrentIndex(1))
ui.settings_button.clicked.connect(lambda: ui.main_display_stack.setCurrentIndex(2))
"""