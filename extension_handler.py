import os

EX_STATIC_KEYWORD = "STATIC"
EX_DEFAULT_KEYWORD = "DEFAULT"

EX_RUN_DOWNTIME = "EX_RUN_DOWNTIME"
EX_RUN_SUSPEND = "EX_RUN_SUSPEND"

class LightsExtensionLoopEvent():
    def __init__(self, proc, ex):
        self.ex = ex
        self.set_proc_if_nec(proc)

    def set_proc_if_nec(self, proc):
        if(self.ex.keyword == EX_STATIC_KEYWORD):
            self.proc = None
            return
        
        if(self.ex.keyword == EX_DEFAULT_KEYWORD):
            self.proc = proc
            return

class LightsExtension:
    def __init__(self, name, keyword, start_fn, loop_fn, stop_fn):
        self.name = name
        self.keyword = keyword
        self.start_fn = start_fn
        self.loop_fn = loop_fn
        self.stop_fn = stop_fn

class LightsExtensionBuilder:
    def __init__(self):
        self.name = None
        self.start_fn = None
        self.loop_fn = None
        self.stop_fn = None
        self.keyword = None
    
    def register_ex(self, name):
        self.name = name

    def register_start(self, start_fn):
        self.start_fn = start_fn

    def register_loop(self, loop_fn):
        self.loop_fn = loop_fn

    def register_stop(self, stop_fn):
        self.stop_fn = stop_fn

    def register_keyword(self, keyword):
        self.keyword = keyword
    
    def build(self):
        ex = LightsExtension(self.name, self.keyword, self.start_fn, self.loop_fn, self.stop_fn)
        return ex

def setup_extensions(glo):
    files = os.listdir(glo.extensions_dir)
    files = [f for f in files if f.endswith(".py") and os.path.isfile(os.path.join(glo.extensions_dir, f))]

    for file in files:

        builder = LightsExtensionBuilder()

        fileText = ""
        with open(os.path.join(glo.extensions_dir, file), "r") as stream:
            fileText = stream.read()

        def exec_scope():
            exec(fileText, {
                "register_ex": builder.register_ex,
                "register_start": builder.register_start,
                "register_loop": builder.register_loop,
                "register_stop": builder.register_stop,
                "register_keyword": builder.register_keyword,
                "EX_STATIC_KEYWORD": EX_STATIC_KEYWORD,
                "EX_DEFAULT_KEYWORD": EX_DEFAULT_KEYWORD,
                "EX_RUN_DOWNTIME": EX_RUN_DOWNTIME,
                "EX_RUN_SUSPEND": EX_RUN_SUSPEND,
            })

        exec_scope()

        try:
            ex = builder.build()
            glo.load_extension(ex)
        except Exception as e:
            print(e)
