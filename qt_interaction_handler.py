def setup_ui_interactions(ui):
    ui.home_button.clicked.connect(lambda: ui.main_display_stack.setCurrentIndex(0))
    ui.action_button.clicked.connect(lambda: ui.main_display_stack.setCurrentIndex(1))
    ui.settings_button.clicked.connect(lambda: ui.main_display_stack.setCurrentIndex(2))