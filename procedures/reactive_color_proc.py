from PyQt5.QtGui import QColor

# set_state MUST BE CALLED
# set_run MUST BE CALLED
def start(set_state, set_run, ex):
    set_state(None)
    set_run(PROC_RUN_DOWNTIME, 1000)

    print(ex)

# set_run MUST BE CALLED
def loop(state, set_run, ex):
    set_run(PROC_RUN_DOWNTIME, 1000)
    #print("LOOPED PROC")

def stop(state, ex):
    #print("STOPPED PROC")
    pass

# LETTER LIGHTS AND PERIMETER LIGHTS ARE THE DOMAINS
register_procedure("Reactive Color V1.0.0", "Changes the color based on sound", ["LL", "PL"])
register_ex("Sound Listener")
register_start(start)
register_loop(loop)
register_stop(stop)
register_color_arg("Color arg", "Pick the color arg", QColor(255, 255, 255, 255))
register_select_arg("Select arg", "Pick the select", ["Coors", "Busch"], "Coors")
register_select_arg("Select arg 2", "Pick 2", ["Hell", "Yeah"], "Hell")
