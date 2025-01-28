import sys
import pygame as pg
import numpy as np
import matplotlib.pylab as pl
from time import time


class Graphics:
    def __init__(self, file, data, video, video_style, colors):
        width = video['width']
        height = video['height']
        fps = video['fps']

        self.colors = colors
        self.options = video_style
        self.file = file
        self.width = width
        self.height = height
        self.data = data
        self.fps = fps
        self.N = len(data)
        self.T = self.N / self.fps

        if self.options["scene"] == "bar":
            self.data = self._bins(self.options["n-bars"])

    def pygame_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

    def draw_fps(self):
        text = "[" + str(int(self.clock.get_fps())) + "fps]"
        text_obj = self.fps_font.render(text, True, self.colors["fps"])
        self.window.blit(text_obj, (7, 7))

    def draw_debug(self, data, n, t, t2):
        texts = \
            f"{n = }",\
            f"{t = :.2f}s of {self.T:.0f}s",\
            f"offset = {t - n / self.fps:.5f}",\
            f"max = {max(data):.3f}",\
            f"music offset {t2}" 
        dy = 14
        for i, text in enumerate(texts):
            text_obj = self.fps_font.render(text, True, self.colors["debug"])
            self.window.blit(text_obj, (7, 7 + (i+1) * dy))

    def draw_graph(self, data, color, size=1, y_offset=0, scale=1):
        """
        data, np.array : data to plot
        color, tuple   : RGB value for graph
        size, int      : graph thickness
        y_offset, int  : y-axis offset for graph
        scale, float   : multiply data by a scalar 
        """
        if size == 0:
            return

        data = data * self.height * scale + y_offset
        x = np.linspace(0, self.width, len(data))
        data = [(xi, -yi + self.height) for xi, yi in zip(x, data)]
        pg.draw.lines(
            surface = self.window,
            color = color,
            closed = False,
            points = data,
            width = size)  

    def draw_graph_frame(self, data):
        self.draw_graph(
            data = data, 
            color = self.colors["shadow"], 
            size = self.options["shadow-size"],
            y_offset = self.options["shadow-offset"],
            scale = self.options["shadow-scale"])
        self.draw_graph(
            data = data,
            color = self.colors["graph"],
            size = self.options["graph-size"],
            y_offset = self.options["graph-offset"]) 
    
    def _bins(self, N):
        """
        Make N bins
        """
        bins = []
        for y in self.data:
            b = []
            l = max(1, len(y) // N)  # length
            for n in range(N):
                avg = sum(y[n*l : (n+1)*l]) / l
                b.append(avg)

            bins.append(np.array(b))

        m = max([max(y) for y in bins])
        return [b / m for b in bins]

    def draw_bar_frame(self, data):
        n = len(data)
        c0, c1 = self.options["bars-crange"]
        colors = [(r, g, b) for r, g, b, _ in  # (r, g, b) color range
                  pl.cm.jet(np.linspace(c0, c1, self.height))*255]
        widths = np.linspace(0, self.width, n+1)
        avg_width = self.width / n

        for i in range(n):
            d = data[i] * self.height
            body = pg.Rect(widths[i], self.height - d, avg_width, d)  # left, top, width, height
            pg.draw.rect(self.window, colors[int(data[i]*self.height)-1], body)

    def draw_main(self, data):
        scenes = {
            "graph": self.draw_graph_frame,
            "bar" : self.draw_bar_frame}
        scenes[self.options["scene"]](data)

    def start(self):
        # initialize
        pg.init()
        self.fps_font = pg.font.SysFont('consas', 18)
        self.clock = pg.time.Clock()
        self.window = pg.display.set_mode((self.width, self.height))

        icon = pg.image.load('icon.png')
        pg.display.set_icon(icon)
        pg.display.set_caption('Sound Visualizer')

        sound = pg.mixer.Sound(self.file)
        sound.play()
        t0 = time()

        while True:
            # calculate timestep based on real-time
            dt2 = pg.mixer.music.get_pos() / 1000
            dt = time() - t0
            n = int(self.fps * dt)

            if n >= self.N:
                pg.quit()
                sys.exit()

            # draw frame
            data = self.data[n]
            self.window.fill(self.colors["window"])
            self.draw_main(data)
            self.draw_fps()
            self.clock.tick(self.fps)
            self.draw_debug(data, n, dt, dt2)
            pg.display.update()
            self.pygame_events()
