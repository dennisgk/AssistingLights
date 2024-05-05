import pyaudio
import math
import time
import numpy as np

# ALL 2 SETS MUST BE CALLED
def start(set_state, set_run):
    st = {}

    st["p"] = pyaudio.PyAudio()
    st["DEF_INFO"] = st["p"].get_default_input_device_info()
    st["FPS"] = 300
    st["frames_per_buffer"] = 1024

    st["stream"] = st["p"].open(format=pyaudio.paInt16,
                    input_device_index=int(st["DEF_INFO"]["index"]),
                    channels=1,
                    rate=int(st["DEF_INFO"]["defaultSampleRate"]),
                    input=True,
                    frames_per_buffer=st["frames_per_buffer"])

    st["db"] = 0

    set_state(st)
    set_run(EX_RUN_DOWNTIME, st["FPS"])

# SET MUST BE CALLED
def loop(state, set_run):
    try:
        y = np.fromstring(state["stream"].read(state["frames_per_buffer"], exception_on_overflow=False), dtype=np.int16)
        y = y.astype(np.float32)
        state["stream"].read(state["stream"].get_read_available(), exception_on_overflow=False)
        
        db = 20 * np.log10(np.sqrt(np.mean(np.abs(y) ** 2)))
        if(math.isfinite(db)):
            state["db"] = db
        
    except:
        pass

    set_run(EX_RUN_DOWNTIME, state["FPS"])

def stop(state):
    state["stream"].stop_stream()
    state["stream"].close()
    state["p"].terminate()

register_ex("Sound Listener")
register_start(start)
register_loop(loop)
register_stop(stop)
register_keyword(EX_STATIC_KEYWORD)
