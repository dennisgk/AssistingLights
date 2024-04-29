import threading
from datetime import datetime

class SyncWaiter():
    def __init__(self):
        self.start_time = datetime.now()

        self.quit_event = threading.Event()

        self.var = []
        self.var_mutex = threading.Lock()
        self.var_event = threading.Event()

        self.downtime_var = []
        self.downtime_var_mutex = threading.Lock()
        self.downtime_var_event = threading.Event()

        self.downtime_thread = threading.Thread(target = self.downtime_waiter)
        self.downtime_thread.start()

    def has_quit(self):
        return self.quit_event.is_set()
        
    def wait_var(self):
        if(self.has_quit()):
            return None

        self.var_mutex.acquire()
        if(len(self.var) > 0):
            return self.var[0]
        
        self.var_mutex.release()

        self.var_event.wait()
        if(self.has_quit()):
            return None
        
        self.var_mutex.acquire()

        return self.var[0]

    def release_var(self):
        self.var.pop(0)
        self.var_mutex.release()

    def set(self, v):
        if(self.has_quit()):
            return

        self.var_mutex.acquire()
        self.var.append(v)
        self.var_mutex.release()
        self.var_event.set()
        self.var_event.clear()

    def set_downtime(self, v, millis):
        if(self.has_quit()):
            return
        
        self.downtime_var_mutex.acquire()
        self.downtime_var.append((self.elapsed_millis() + millis, v))
        self.downtime_var_mutex.release()
        self.downtime_var_event.set()
        self.downtime_var_event.clear()

    def elapsed_millis(self):
        dt = datetime.now() - self.start_time
        ms = (dt.days * 24 * 60 * 60 + dt.seconds) * 1000 + dt.microseconds / 1000.0
        return ms

    def quit(self):
        self.quit_event.set()

        self.var_event.set()
        self.var_event.clear()
        self.downtime_var_event.set()
        self.downtime_var_event.clear()

    def downtime_waiter(self):

        ordered_waitings = []

        while True:
            if(self.has_quit()):
                break

            if(len(ordered_waitings) > 0):
                is_event_set = self.downtime_var_event.wait((ordered_waitings[0][0] - self.elapsed_millis()) * 0.001)
                if(self.has_quit()):
                    break

                if(is_event_set):
                    self.downtime_var_mutex.acquire()
                    ordered_waitings.extend(self.downtime_var)
                    ordered_waitings.sort(key = lambda x: x[0])

                    self.downtime_var = []
                    self.downtime_var_mutex.release()
            else:
                self.downtime_var_event.wait()
                if(self.has_quit()):
                    break

                self.downtime_var_mutex.acquire()
                ordered_waitings = self.downtime_var
                ordered_waitings.sort(key = lambda x: x[0])

                self.downtime_var = []
                self.downtime_var_mutex.release()

            del_ordered_index = len(ordered_waitings)

            for x in range(0, len(ordered_waitings)):
                if(self.elapsed_millis() >= ordered_waitings[x][0]):
                    self.set(ordered_waitings[x][1])
                else:
                    del_ordered_index = x
                    break

            for x in range(0, del_ordered_index):
                ordered_waitings.pop(0)
