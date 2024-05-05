import time
import numpy as np
import pyaudio

# ALL 2 SETS MUST BE CALLED
def start(set_state, set_run):
    st = {}

    st["MIC_RATE"] = 48000
    st["FPS"] = 50

    st["p"] = pyaudio.PyAudio()
    st["frames_per_buffer"] = st["MIC_RATE"] / st["FPS"]

    st["stream"] = st["p"].open(format=pyaudio.paInt16,
                    channels=1,
                    rate=st["MIC_RATE"],
                    input=True,
                    frames_per_buffer=st["frames_per_buffer"])
    
    st["overflows"] = 0
    st["prev_ovf_time"] = time.time()

    st["y"] = 0

    set_state(st)
    set_run(EX_RUN_DOWNTIME, st["FPS"])

# SET MUST BE CALLED
def loop(state, set_run):
    try:
        y = np.fromstring(state["stream"].read(state["frames_per_buffer"], exception_on_overflow=False), dtype=np.int16)
        y = y.astype(np.float32)
        state["stream"].read(state["stream"].get_read_available(), exception_on_overflow=False)
        state["y"] = y
    except:
        state["overflows"] += 1
        if time.time() > state["prev_ovf_time"] + 1:
            state["prev_ovf_time"] = time.time()

            num_overflows = state["overflows"]
            print(f"Audio buffer has overflowed {num_overflows} times.")

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
