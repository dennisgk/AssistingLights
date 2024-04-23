
def start():
    pass

def loop():
    pass

def stop():
    pass

register_procedure("Reactive Color", "Changes the color based on sound", ["LETTER LIGHTS", "PERIMETER LIGHTS"])
register_ex("Basic Ex")
register_start(start)
register_loop(loop)
register_stop(stop)
register_color_arg("Color arg", "Pick the color arg", QColor(255, 255, 255, 255))
register_select_arg("Select arg", "Pick the select", ["Coors", "Busch"], "Coors")

del start
del loop
del stop