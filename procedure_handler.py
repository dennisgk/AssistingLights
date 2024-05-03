import os

PROC_RUN_QUIT = "PROC_RUN_QUIT"
PROC_RUN_DOWNTIME = "PROC_RUN_DOWNTIME"
PROC_RUN_SUSPEND = "PROC_RUN_SUSPEND"

class LightsProcedureInitializeEvent():
    def __init__(self, proc, args):
        self.proc = proc
        self.args = args

class LightsProcedure:
    def __init__(self, name, desc, domains, ex, start_fn, loop_fn, stop_fn, args):
        self.name = name
        self.desc = desc
        self.domains = domains
        self.ex = ex
        self.start_fn = start_fn
        self.loop_fn = loop_fn
        self.stop_fn = stop_fn
        self.args = args

class LightsProcedureSelectArg():
    def __init__(self, name, desc, select_options, select_def):
        self.name = name
        self.desc = desc
        self.select_options = select_options
        self.select_def = select_def

class LightsProcedureColorArg():
    def __init__(self, name, desc, color_def):
        self.name = name
        self.desc = desc
        self.color_def = color_def

class LightsProcedureBuilder:
    def __init__(self):
        self.name = None
        self.desc = None
        self.domains = None
        self.ex = []
        self.start_fn = None
        self.loop_fn = None
        self.stop_fn = None
        self.args = []

    def register_procedure(self, name, desc, domains):
        self.name = name
        self.desc = desc
        self.domains = domains

    def register_ex(self, ex_name):
        self.ex.append(ex_name)

    def register_start(self, start_fn):
        self.start_fn = start_fn

    def register_loop(self, loop_fn):
        self.loop_fn = loop_fn

    def register_stop(self, stop_fn):
        self.stop_fn = stop_fn

    def register_color_arg(self, arg_name, arg_desc, arg_color_def):
        arg = LightsProcedureColorArg(arg_name, arg_desc, arg_color_def)
        self.args.append(arg)

    def register_select_arg(self, arg_name, arg_desc, arg_select_options, arg_select_def):
        arg = LightsProcedureSelectArg(arg_name, arg_desc, arg_select_options, arg_select_def)
        self.args.append(arg)

    def build(self):
        proc = LightsProcedure(self.name, self.desc, self.domains, self.ex, self.start_fn, self.loop_fn, self.stop_fn, self.args)
        return proc

def setup_procedures(glo):
    files = os.listdir(glo.procedures_dir)
    files = [f for f in files if f.endswith(".py") and os.path.isfile(os.path.join(glo.procedures_dir, f))]

    for file in files:

        builder = LightsProcedureBuilder()

        fileText = ""
        with open(os.path.join(glo.procedures_dir, file), "r") as stream:
            fileText = stream.read()

        exec(fileText, {
            "register_procedure": builder.register_procedure,
            "register_ex": builder.register_ex,
            "register_start": builder.register_start,
            "register_loop": builder.register_loop,
            "register_stop": builder.register_stop,
            "register_color_arg": builder.register_color_arg,
            "register_select_arg": builder.register_select_arg,
            "PROC_RUN_QUIT": PROC_RUN_QUIT,
            "PROC_RUN_DOWNTIME": PROC_RUN_DOWNTIME,
            "PROC_RUN_SUSPEND": PROC_RUN_SUSPEND
        })

        try:
            proc = builder.build()
            glo.load_procedure(proc)
        except Exception as e:
            print(e)
