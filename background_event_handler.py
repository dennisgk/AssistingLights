from procedure_handler import LightsProcedureInitializeEvent

def write_to_output(glo, text):
    glo.ui.output_text_edit.insertHtml(f"<span style=\"color:blue;\">{text}</span><br />")

def write_to_error(glo, text):
    glo.ui.output_text_edit.insertHtml(f"<span style=\"background-color:#f5060f;color:#fafafa;\">{text}</span><br />")

def handle_background_event(glo, ev, update_ui):

    if(isinstance(ev, LightsProcedureInitializeEvent)):
        proc_run = []

        domains_comp = []

        for key in glo.proc_states:
            domains_comp.extend(key.domains)

        if(any(proc_domain in domains_comp for proc_domain in ev.proc.domains)):
            update_ui(lambda: write_to_error(glo, f"Procedure \"{ev.proc.name}\" has a "
                "domain shared with another procedure running. Stop the other procedure first."))

        def proc_set_state(state):
            glo.proc_states[ev.proc] = state
        
        def proc_set_run(*args):
            proc_run.extend(args)

        ev.proc.start_fn(proc_set_state, proc_set_run)

