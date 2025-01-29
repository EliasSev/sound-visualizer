import toml
import argparse
from pathlib import Path
from src.soundvis.soundvisualizer import SoundVis
from src.soundvis.graphics import Graphics


def parse_input():
    parser = argparse.ArgumentParser(
        description="Sound visualizer: Specify an audio file andvisualize the frequency spectrum.")
    parser.add_argument(
        '-f', '--file',
        default='C418-Wet-Hands.mp3',
        metavar='',
        help="Specify the name of the audio file")
    parser.add_argument(
        '-c', '--config',
        default='example.toml',
        metavar='',
        help="Specify name of a configuration file to modify the visuals")
    args = parser.parse_args()
    path = Path(args.file)
    config = Path(args.config)

    return str(path.resolve()), str(config.resolve())


def fill_default_values(config, default_config):
    for key, value in default_config.items():
        config_value = config.get(key)
        if config_value is None:
            config[key] = value
    return config


def read_config(toml_path):
    if toml_path is None:
        config = {}
    else: 
        with open(toml_path, 'r') as file:
            config = toml.load(file)
    
    processing_default = {
        'window': 0.06,
        'scaling': 0.75,
        'smoothing': 2,
        'n-smooth': 2,
        'span-hz': (0, 4000),
        'time-smoothing': 2,
        'stop-time': None}
    video_default = {
        'width': 1200,
        'height': 800,
        'fps': 60}
    video_style_default = {
        'scene': 'bar',
        'graph-size': 5,
        'graph-offset': 20,
        'shadow-size': 0,
        'shadow-offset': 15,
        'shadow-scale': 0.7,
        'n-bars': 100,
        'bars-crange': (0.0, 0.6),
        'color-map': 'viridis',
        'colors-only': False}
    color_default = {
        'graph': (0, 255, 0),
        'shadow': (255, 0, 0),
        'window': (0, 0, 0),
        'fps': (255, 255, 255),
        'debug': (255, 255, 255)}

    # [processing]
    processing = config.get('processing', {})
    processing = fill_default_values(processing, processing_default)

    # [video]
    video = config.get('video', {})
    video = fill_default_values(video, video_default)

    # [video-style]
    video_style = config.get('video-style', {})
    video_style = fill_default_values(video_style, video_style_default)

    # [colors]
    colors = config.get('colors', {})
    colors = fill_default_values(colors, color_default)

    return processing, video, video_style, colors


if __name__ == '__main__':
    audio_file_path, config_path = parse_input()
    processing, video, video_style, colors = read_config(config_path)
    soundvis = SoundVis(file=str(audio_file_path),
                        fps=video['fps'],
                        processing=processing)
    graphics = Graphics(file=audio_file_path,
                        data=soundvis.f_hats,
                        video=video,
                        video_style=video_style,
                        colors=colors)
    graphics.start()
