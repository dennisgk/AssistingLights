from PyQt5.QtGui import QColor
import time
import os

strip_control = None

"""
If you are using an earlier Raspberry Pi single board computer (a Raspberry Pi 3 Model B, 3B+ this has been identified for) and only one or two LEDs turn on when you run this script (and they flicker or show odd colours) do the following to fix it. Type and enter | sudo nano /boot/config.txt |. This will open up inside the terminal command a text editor. Using the arrow keys navigate to the section that states | dtparam=audio=on | and change it to | dtparam=audio=off |. With that completed press | Ctrl + X | and then | Y | to save the changes and exit.
"""

if os.name == "nt":
    class StripControlImitator:
        def PixelStrip(*args):
            return StripControlImitator()
        
        def begin(*args):
            pass

        def fill(*args):
            pass

        def Color(*args):
            pass

        def setPixelColor(*args):
            pass

        def show(*args):
            pass

    strip_control = StripControlImitator()
else:
    import rpi_ws281x
    strip_control = rpi_ws281x

# set_state MUST BE CALLED
# set_run MUST BE CALLED
def start(set_state, set_run, args, ex):
    state = {}

    state["LED_COUNT"] = 30
    state["LED_PIN"] = 18
    state["LED_FREQ_HZ"] = 800000
    state["LED_DMA"] = 10
    state["LED_BRIGHTNESS"] = 255
    state["LED_INVERT"] = False
    state["LED_CHANNEL"] = 0
    state["FPS"] = 100

    state["default_color"] = [args["Color arg"].red(), args["Color arg"].green(), args["Color arg"].blue()]

    state["strip"] = strip_control.PixelStrip(state["LED_COUNT"], state["LED_PIN"], state["LED_FREQ_HZ"], state["LED_DMA"], state["LED_INVERT"], state["LED_BRIGHTNESS"], state["LED_CHANNEL"])
    state["strip"].begin()

    set_state(state)
    set_run(PROC_RUN_DOWNTIME, state["FPS"])

# set_run MUST BE CALLED
def loop(state, set_run, ex):
    adj_db = max(ex["Sound Listener"]["db"] - 40, 0)
    color = [int(min(255, col * adj_db**2 / (80**2))) for col in state["default_color"]]

    for x in range(0, state["LED_COUNT"]):
        state["strip"].setPixelColor(x, strip_control.Color(color[0], color[1], color[2]))
    state["strip"].show()

    set_run(PROC_RUN_DOWNTIME, state["FPS"])

def stop(state, ex):
    for x in range(0, state["LED_COUNT"]):
        state["strip"].setPixelColor(x, strip_control.Color(0, 0, 0))
    
    state["strip"].show()

# LETTER LIGHTS AND PERIMETER LIGHTS ARE THE DOMAINS
register_procedure("Reactive Color V1.0.0", "Changes the color based on sound", ["LL", "PL"])
register_ex("Sound Listener")
register_start(start)
register_loop(loop)
register_stop(stop)
register_color_arg("Color arg", "Pick the color arg", QColor(255, 255, 255, 255))
register_select_arg("Select arg", "Pick the select", ["Coors", "Busch"], "Coors")
register_select_arg("Select arg 2", "Pick 2", ["Hell", "Yeah"], "Hell")
