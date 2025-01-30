import toml
import argparse
from pathlib import Path


class ConfigManager:
    DEFAULTS = {
        'processing': {
            'window': 0.06,
            'scaling': 0.75,
            'smoothing': 2,
            'n-smooth': 2,
            'span-hz': (0, 4000),
            'time-smoothing': 2,
            'stop-time': None},
        'video': {
            'width': 1200,
            'height': 800,
            'fps': 60},
        'video-style': {
            'scene': 'bar',
            'graph-size': 5,
            'graph-offset': 20,
            'shadow-size': 0,
            'shadow-offset': 15,
            'shadow-scale': 0.7,
            'n-bars': 100,
            'color-map': 'viridis',
            'colors-only': False},
        'colors': {
            'graph': (0, 255, 0),
            'shadow': (255, 0, 0),
            'window': (0, 0, 0),
            'fps': (255, 255, 255),
            'debug': (255, 255, 255)}}
    
    def __init__(self):
        args = self._parse_input()
        self._file_path = str(Path(args.file).resolve())
        self._config_path = str(Path(args.config).resolve())
        self._config = self._read_config(self.config_path)

    @property
    def file_path(self):
        return self._file_path
    
    @property
    def config_path(self):
        return self._config_path
    
    @property
    def config(self):
        return self._config

    def _parse_input(self):
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
        return parser.parse_args()

    def _read_config(self, config_path):
        with open(config_path, 'r') as f:
            config = toml.load(f)
        return self._merge_dicts(self.DEFAULTS, config)
    
    def _merge_dicts(self, default, config):
        merged = default.copy()
        for key, value in config.items():
            if (key in merged) and isinstance(value, dict):
                merged[key] = self._merge_dicts(merged[key], value)
            else:
                merged[key] = value
        return merged
    

