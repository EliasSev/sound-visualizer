from src.soundvisualizer import SoundVis
from src.graphics import Graphics

"""
## TODO ##
- bar graph
- slight offsync (video behind)
"""

if __name__ == '__main__':
    track = "tracks/TetrisTheme.wav"
    fps = 60
    sound = SoundVis(
        file = track,
        fps = fps,
        s_width = 0.06,     # audio slice width in seconds (to apply FFT on)
        scaling = 0.75,     # 0 to 1, the lower the number to more downscaling is applied
        smoothing = 2,      # width of convolution, 0 for no smoothing
        nsmooth = 3,        # number of interations to apply smoothing
        span = (0, 4000),   # range in Hz
        time_smoothing = 2  # number of previous frames to smooth with
        )
    graphics = Graphics(
        file = track,
        data = sound.f_hats,
        width = 1200, 
        height = 800, 
        fps = fps,
        colors = {
            "graph": (0, 0, 255),
            "shadow": (255, 0, 0),
            "window": (0, 0, 0),
            "fps": (255, 255, 255),
            "debug": (255, 255, 255)
            },
        options = {
            "scene" : "bar",  # graph, bar
            "graph-size": 5,
            "graph-offset" : 20,
            "shadow-size": 0,  # 0 to turn off
            "shadow-offset": 15,
            "shadow-scale": 0.7,
            "N-bars" : 75,
            "bars-crange" : (0, .6)  # color range, 0 to 1
            }
        )
    graphics.start()
