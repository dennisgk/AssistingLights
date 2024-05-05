from procedure_handler import LightsProcedureStartEvent, LightsProcedureLoopEvent, LightsProcedureStopEvent, PROC_RUN_DOWNTIME, PROC_RUN_QUIT, PROC_RUN_SUSPEND
from extension_handler import EX_STATIC_KEYWORD, EX_DEFAULT_KEYWORD, EX_RUN_DOWNTIME, EX_RUN_SUSPEND, LightsExtensionLoopEvent
from PyQt5.QtWidgets import QTreeWidgetItem, QPushButton
from PyQt5 import QtCore
from qt_handler import generate_simple_wrap_label, set_widget_text

def write_to_output(glo, text):
    glo.ui.output_text_edit.insertHtml(f"<span style=\"color:#FAFAFA;\">{text}</span><br />")

def write_to_error(glo, text):
    glo.ui.output_text_edit.insertHtml(f"<span style=\"background-color:#f5060f;color:#fafafa;\">{text}</span><br />")

def remove_tree_row(glo, proc):
    
    for x in range(0, glo.ui.info_tree_view.topLevelItemCount()):
        if glo.ui.info_tree_view.topLevelItem(x).data(0, 0) != proc:
            continue

        glo.ui.info_tree_view.takeTopLevelItem(x)


def add_tree_row(glo, proc, debug_callback, stop_callback):
    row_root = QTreeWidgetItem(glo.ui.info_tree_view)
    row_root_label = generate_simple_wrap_label(proc.name)

    row_root.setData(0, 0, proc)

    domains_child = QTreeWidgetItem()
    domains_child_label = generate_simple_wrap_label("Domains")
    domains_child_text = generate_simple_wrap_label(", ".join(proc.domains))

    debug_child = QTreeWidgetItem()
    debug_child_label = generate_simple_wrap_label("Debug")
    debug_child_button = QPushButton()
    debug_child_button.setStyleSheet("QPushButton {\n"
"    border: none;\n"
"    background-color: rgb(35, 83, 71);\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: rgb(33, 37, 43);\n"
"}\n"
"QPushButton:pressed {    \n"
"    background-color: rgb(85, 170, 255);\n"
"}")
    set_widget_text(debug_child_button, "Dump Info")
    debug_child_button.clicked.connect(debug_callback)

    stop_child = QTreeWidgetItem()
    stop_child_label = generate_simple_wrap_label("Stop")
    stop_child_button = QPushButton()
    stop_child_button.setStyleSheet("QPushButton {\n"
"    border: none;\n"
"   background-color: rgb(240, 30, 30);\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: rgb(220, 10, 10);\n"
"}\n"
"QPushButton:pressed {    \n"
"    background-color: rgb(85, 170, 255);\n"
"}")
    set_widget_text(stop_child_button, "Send Stop")
    stop_child_button.clicked.connect(stop_callback)

    row_root.addChild(domains_child)
    row_root.addChild(debug_child)
    row_root.addChild(stop_child)

    glo.ui.info_tree_view.addTopLevelItem(row_root)
    glo.ui.info_tree_view.setItemWidget(row_root, 0, row_root_label)

    glo.ui.info_tree_view.setItemWidget(domains_child, 0, domains_child_label)
    glo.ui.info_tree_view.setItemWidget(domains_child, 1, domains_child_text)

    glo.ui.info_tree_view.setItemWidget(stop_child, 0, stop_child_label)
    glo.ui.info_tree_view.setItemWidget(stop_child, 1, stop_child_button)

    glo.ui.info_tree_view.setItemWidget(debug_child, 0, debug_child_label)
    glo.ui.info_tree_view.setItemWidget(debug_child, 1, debug_child_button)

def get_extension_state(glo, proc, ex):
    ex_state = None

    if ex.keyword == EX_STATIC_KEYWORD:
        ex_state = glo.ex_states[ex]

    if ex.keyword == EX_DEFAULT_KEYWORD:
        ex_state = glo.ex_states[(proc, ex)]

    return ex_state

def get_extensions_object(glo, proc):
    ex_list = {}
    ex_all_vals = [ex_poss for ex_poss in glo.extensions if ex_poss.name in proc.ex]

    for ex_val in ex_all_vals:
        ex_list[ex_val.name] = get_extension_state(glo, proc, ex_val)
    
    return ex_list

def stop_proc(glo, proc):
    glo.background_dispatch_loop.remove_where(lambda x: (isinstance(x, LightsProcedureLoopEvent) and x.proc == proc) or \
                                            (isinstance(x, LightsProcedureStopEvent) and x.proc == proc))
    proc.stop_fn(glo.proc_states[proc], get_extensions_object(glo, proc))
    
    stop_proc_all_ex(glo, proc)
    glo.proc_states.pop(proc, None)

def stop_proc_all_ex(glo, proc):
    ex_vals_all = [ex_poss for ex_poss in glo.extensions if ex_poss.name in proc.ex]
    other_procs_all = [other for other in list(glo.proc_states.keys()) if other != proc]

    for ex in ex_vals_all:
        state_key = None

        if(ex.keyword == EX_STATIC_KEYWORD):
            other_proc_relies = any([ex.name in other_proc.ex for other_proc in other_procs_all])
            if(other_proc_relies):
                continue

            state_key = ex
        
        if(ex.keyword == EX_DEFAULT_KEYWORD):
            state_key = (proc, ex)

        glo.background_dispatch_loop.remove_where(lambda x: isinstance(x, LightsExtensionLoopEvent) and x.ex == ex)

        ex.stop_fn(glo.ex_states[state_key])
        glo.ex_states.pop(state_key, None)

def start_proc_all_ex(glo, proc):
    ex_vals_all = [ex_poss for ex_poss in glo.extensions if ex_poss.name in proc.ex]

    for ex in ex_vals_all:
        state_key = None

        if(ex.keyword == EX_STATIC_KEYWORD):
            if(ex in glo.ex_states):
                continue
            state_key = ex

        if(ex.keyword == EX_DEFAULT_KEYWORD):
            state_key = (proc, ex)
        
        ex_run = []

        def ex_set_state(state):
            glo.ex_states[state_key] = state
        
        def ex_set_run(*args):
            ex_run.extend(args)

        ex.start_fn(ex_set_state, ex_set_run)

        if len(ex_run) > 0:
            if(ex_run[0] == EX_RUN_DOWNTIME):
                glo.background_dispatch_loop.set_downtime(LightsExtensionLoopEvent(proc, ex), ex_run[1])
                continue

            if(ex_run[0] == EX_RUN_SUSPEND):
                continue

def handle_background_event(glo, ev, update_ui):

    if(isinstance(ev, LightsProcedureStartEvent)):

        # make sure its not interfering with other domains
        domains_comp = []

        for key in glo.proc_states:
            domains_comp.extend(key.domains)

        if(any([proc_domain in domains_comp for proc_domain in ev.proc.domains])):
            update_ui(lambda: write_to_error(glo, f"Procedure <b>{ev.proc.name}</b> has a "
                "domain shared with another procedure running. Stop the other procedure first."))
            return

        # add and setup extensions

        def on_proc_debug():
            debug_obj = {}
            debug_obj["Procedure State"] = glo.proc_states[ev.proc]
            debug_obj["Extension States"] = {}

            debug_ex_obj = get_extensions_object(glo, ev.proc)
            for ex_key in debug_ex_obj:
                debug_obj["Extension States"][ex_key] = debug_ex_obj[ex_key]

            write_to_output(glo, str(debug_obj))

        def on_proc_stop():
            glo.background_dispatch_loop.set(LightsProcedureStopEvent(ev.proc))

        update_ui(lambda: add_tree_row(glo, ev.proc, on_proc_debug, on_proc_stop))

        start_proc_all_ex(glo, ev.proc)

        # run the procedure

        proc_run = []
        
        def proc_set_state(state):
            glo.proc_states[ev.proc] = state
        
        def proc_set_run(*args):
            proc_run.extend(args)
            
        ev.proc.start_fn(proc_set_state, proc_set_run, ev.args, get_extensions_object(glo, ev.proc))

        if len(proc_run) > 0:
            if(proc_run[0] == PROC_RUN_QUIT):
                update_ui(lambda: write_to_error(f"Procedure <b>{ev.proc.name}</b> quit itself."))
                glo.background_dispatch_loop.set(LightsProcedureStopEvent(ev.proc))
                return

            if(proc_run[0] == PROC_RUN_DOWNTIME):
                glo.background_dispatch_loop.set_downtime(LightsProcedureLoopEvent(ev.proc), proc_run[1])
                return

            if(proc_run[0] == PROC_RUN_SUSPEND):
                return
            
        return
    
    if(isinstance(ev, LightsProcedureLoopEvent)):
        proc_run = []
        
        def proc_set_run(*args):
            proc_run.extend(args)

        ev.proc.loop_fn(glo.proc_states[ev.proc], proc_set_run, get_extensions_object(glo, ev.proc))
            
        if len(proc_run) > 0:
            if(proc_run[0] == PROC_RUN_QUIT):
                update_ui(lambda: write_to_error(f"Procedure <b>{ev.proc.name}</b> quit itself."))
                glo.background_dispatch_loop.set(LightsProcedureStopEvent(ev.proc))
                return

            if(proc_run[0] == PROC_RUN_DOWNTIME):
                glo.background_dispatch_loop.set_downtime(LightsProcedureLoopEvent(ev.proc), proc_run[1])
                return

            if(proc_run[0] == PROC_RUN_SUSPEND):
                return
            
        return

    if(isinstance(ev, LightsProcedureStopEvent)):
        stop_proc(glo, ev.proc)
        update_ui(lambda: remove_tree_row(glo, ev.proc))

        return

    if(isinstance(ev, LightsExtensionLoopEvent)):
        ex_run = []
        
        def ex_set_run(*args):
            ex_run.extend(args)

        ev.ex.loop_fn(get_extension_state(glo, ev.proc, ev.ex), ex_set_run)
        
        if len(ex_run) > 0:
            if(ex_run[0] == EX_RUN_DOWNTIME):
                glo.background_dispatch_loop.set_downtime(LightsExtensionLoopEvent(ev.proc, ev.ex), ex_run[1])
                return

            if(ex_run[0] == EX_RUN_SUSPEND):
                return
            
        return
