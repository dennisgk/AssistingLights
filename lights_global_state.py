from enum import Enum
import threading
from qt_sync import SyncWaiter
from background_event_handler import handle_background_event
from procedure_handler import LightsProcedureStartEvent
from PyQt5.QtCore import QObject, QThread, pyqtSignal
import os

# updates:
# actually pass extensions into start, loop, and stop functions of procedures
# ^ fixed as of rn other than considering making functions in background_event_handler to better manage stop/start
# for quick quit after start make sure to also exit the necessary extensions
# load extensions! - as in start/stop them when procedures start/stop

class BackgroundDispatchWorker(QThread):
    update_ui = pyqtSignal(object)

    def __init__(self, par):
        super().__init__(None)
        self.par = par

    def run(self):
        self.background_loop()

    def emit_update_ui(self, callback):
        self.update_ui.emit(callback)
        
    def background_loop(self):
        while True:
            ev = self.par.background_dispatch_loop.wait_var()
            if(self.par.background_dispatch_loop.has_quit()):
                break

            handle_background_event(self.par, ev, self.emit_update_ui)

class LightsGlobalState:
    def __init__(self, app, ui, dir):
        self.app = app
        self.ui = ui

        self.procedures_dir = os.path.join(dir, "procedures")
        self.extensions_dir = os.path.join(dir, "extensions")

        self.procedures = []
        self.extensions = []
        
        self.config_arg_passed = None
        self.config_proc = None

        self.proc_states = {}
        self.ex_states = {}

        self.background_dispatch_loop = SyncWaiter()

        self.background_dispatch_thread = BackgroundDispatchWorker(self)
        self.background_dispatch_thread.update_ui.connect(self.connect_update_ui)
        self.background_dispatch_thread.start()

    def connect_update_ui(self, callback):
        callback()

    def load_procedure(self, proc):
        if(any([loaded_proc.name == proc.name for loaded_proc in self.procedures])):
            return
        
        ex_valid = True

        for ex in proc.ex:
            if(not any([loaded_ex.name == ex for loaded_ex in self.extensions])):
                ex_valid = False
                break
        
        if(not ex_valid):
            return

        self.procedures.append(proc)

    def load_extension(self, ex):
        if(any([loaded_ex.name == ex.name for loaded_ex in self.extensions])):
            return

        self.extensions.append(ex)

    def quit_background_dispatch(self):
        self.background_dispatch_loop.quit()

    def run_procedure(self, proc, args):
        ev = LightsProcedureStartEvent(proc, args)
        self.background_dispatch_loop.set(ev)
