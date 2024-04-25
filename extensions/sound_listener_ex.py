def start(set_state, set_keyword, set_run):
    set_state(None)
    set_keyword(EX_STATIC_KEYWORD)
    set_run(PROC_RUN_DOWNTIME, 100)

def loop(state, set_run):
    set_run(PROC_RUN_DOWNTIME, 100)

def stop(state):
    pass

register_ex("Sound Listener")
register_start(start)
register_loop(loop)
register_stop(stop)

del start
del loop
del stop