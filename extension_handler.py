import os

EX_CONST_KEYWORD = "CONST"
EX_STATIC_KEYWORD = "STATIC"
EX_DEFAULT_KEYWORD = "DEFAULT"

EX_RUN_DOWNTIME = "EX_RUN_DOWNTIME"
EX_RUN_SUSPEND = "EX_RUN_SUSPEND"
EX_RUN_IMMEDIATELY = "EX_RUN_IMMEDIATELY"

class LightsExtension:
    def __init__(self, name, start_fn, loop_fn, stop_fn):
        self.name = name
        self.start_fn = start_fn
        self.loop_fn = loop_fn
        self.stop_fn = stop_fn

class LightsExtensionBuilder:
    def __init__(self):
        self.name = None
        self.start_fn = None
        self.loop_fn = None
        self.stop_fn = None
    
    def register_ex(self, name):
        self.name = name

    def register_start(self, start_fn):
        self.start_fn = start_fn

    def register_loop(self, loop_fn):
        self.loop_fn = loop_fn

    def register_stop(self, stop_fn):
        self.stop_fn = stop_fn
    
    def build(self):
        ex = LightsExtension(self.name, self.start_fn, self.loop_fn, self.stop_fn)
        return ex

def setup_extensions(glo):
    files = os.listdir(glo.extensions_dir)
    files = [f for f in files if f.endswith(".py") and os.path.isfile(os.path.join(glo.extensions_dir, f))]

    for file in files:

        builder = LightsExtensionBuilder()

        fileText = ""
        with open(os.path.join(glo.extensions_dir, file), "r") as stream:
            fileText = stream.read()

        exec(fileText, {
            "register_ex": builder.register_ex,
            "register_start": builder.register_start,
            "register_loop": builder.register_loop,
            "register_stop": builder.register_stop,
            "EX_CONST_KEYWORD": EX_CONST_KEYWORD,
            "EX_STATIC_KEYWORD": EX_STATIC_KEYWORD,
            "EX_DEFAULT_KEYWORD": EX_DEFAULT_KEYWORD,
            "EX_RUN_DOWNTIME": EX_RUN_DOWNTIME,
            "EX_RUN_SUSPEND": EX_RUN_SUSPEND,
            "EX_RUN_IMMEDIATELY": EX_RUN_IMMEDIATELY
        })

        try:
            ex = builder.build()
            glo.load_extension(ex)
        except Exception as e:
            print(e)
