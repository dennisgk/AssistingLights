from enum import Enum
import os

class LightsPage(Enum):
    Home = 0
    Action = 1
    Settings = 2
    Config = 3

class LightsGlobalState:
    def __init__(self, app, ui, dir):
        self.app = app
        self.ui = ui

        self.procedures_dir = os.path.join(dir, "procedures")
        self.extensions_dir = os.path.join(dir, "extensions")

        self.procedures = []
        self.extensions = []
    
    def get_page(self):
        index = self.ui.main_display_stack.currentIndex()

        return LightsPage(index)

    def set_page(self, page):
        self.ui.main_display_stack.setCurrentIndex(page.value)

    def load_procedure(self, proc):
        pass

    def load_extension(self, ex):
        pass