# Sound Visualizer
Visualize the frequency spectrum of any soundtrack (mp3 or wav) live.

# Usage
Add any mp3 or wav file into the /tracks folder and change the name of the track variable in main.py file.

# SoundVis parameters
The SoundVis class comes with many customizable parameters:
 - s_width, float: The width of the current chunk of sound being plotted. (ex. 0.06 means that +-0.003 seconds of the past/future is being plotted)
 - scaling, float. Multiply the graph by this number. Used to downscale dominant frequencies (ex. 0.5 will take the square root of all values)
 - smoothing, int. Preform a convolution to smoothen the graph (ex. 3 will use a box of size 3 in the convolution)
 - span, tuple: Range of frequency spectrum in Hz.
 - time_smoothing, int: Take a weighted average of the last few frames for a softer animation.

# Options
Customize the graphics, current available options are
- scene: "graph" or "bar". Change the plotting style
- graph-size: int. Size of graph, 0 and up.
- shadow-size: int. Size of shadow-graph, 0 and up.
- shadow-offset: int. Move the shadow below the graph.
- shadow-scale: float. Scale the shadow up or down (ex. 0.5 will half the values)
- N-bars: int. Number of bars to use in bar style.
- bars-crange: tuple. Colour range of bars, 0 (blue) to 1 (red)

# Dependencies
OBS! Librosa's read method does not work with numpy 2.0 for mp3 files! If you want to use a mp3 file, either downgrade numpy or convert the file to .wav.

 - numpy (not 2.0 or newer)
 - scipy
 - matplotlib
 - pygame
 - librosa