from PyQt5.QtGui import QColor

def start(set_state, set_run):
    set_state(None)
    set_run(PROC_RUN_DOWNTIME, 100)

def loop(state, set_run):
    set_run(PROC_RUN_DOWNTIME, 100)

def stop(state):
    pass

register_procedure("Reactive Color", "Changes the color based on sound", ["LETTER LIGHTS", "PERIMETER LIGHTS"])
register_ex("Sound Listener")
register_start(start)
register_loop(loop)
register_stop(stop)
register_color_arg("Color arg", "Pick the color arg", QColor(255, 255, 255, 255))
register_select_arg("Select arg", "Pick the select", ["Coors", "Busch"], "Coors")

del start
del loop
del stop