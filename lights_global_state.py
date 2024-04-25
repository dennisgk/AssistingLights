from enum import Enum
import os

class LightsGlobalState:
    def __init__(self, app, ui, dir):
        self.app = app
        self.ui = ui

        self.procedures_dir = os.path.join(dir, "procedures")
        self.extensions_dir = os.path.join(dir, "extensions")

        self.procedures = []
        self.extensions = []

    def load_procedure(self, proc):
        self.procedures.append(proc)

    def load_extension(self, ex):
        self.extensions.append(ex)