# ALL 2 SETS MUST BE CALLED
def start(set_state, set_run):
    set_state(69)
    set_run(EX_RUN_DOWNTIME, 1000)

# SET MUST BE CALLED
def loop(state, set_run):
    set_run(EX_RUN_DOWNTIME, 1000)
    print("LOOPED SOUND")

def stop(state):
    print("STOPPED SOUND")

register_ex("Sound Listener")
register_start(start)
register_loop(loop)
register_stop(stop)
register_keyword(EX_STATIC_KEYWORD)

del start
del loop
del stop