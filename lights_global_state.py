from enum import Enum
import threading
from qt_sync import SyncWaiter
from background_event_handler import handle_background_event
import os

class LightsGlobalState:
    def __init__(self, app, ui, dir):
        self.app = app
        self.ui = ui

        self.procedures_dir = os.path.join(dir, "procedures")
        self.extensions_dir = os.path.join(dir, "extensions")

        self.procedures = []
        self.extensions = []
        
        self.config_arg_passed = {}
        self.config_proc = None

        self.background_dispatch_loop = SyncWaiter()

        self.background_dispatch_thread = threading.Thread(target = self.background_loop)
        self.background_dispatch_thread.start()

    def load_procedure(self, proc):
        self.procedures.append(proc)

    def load_extension(self, ex):
        self.extensions.append(ex)

    def quit_background_dispatch(self):
        self.background_dispatch_loop.quit()

    def background_loop(self):

        self.background_dispatch_loop.set_downtime(69, 2000)
        self.background_dispatch_loop.set_downtime(70, 2001)
        self.background_dispatch_loop.set_downtime(1, 1000)

        while True:
            ev = self.background_dispatch_loop.wait_var()
            if(self.background_dispatch_loop.has_quit()):
                break

            handle_background_event(self, ev)
            self.background_dispatch_loop.release_var()