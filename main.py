from src.soundvis.soundvisualizer import SoundVis
from src.soundvis.graphics import Graphics
from src.soundvis.configmanager import ConfigManager


if __name__ == '__main__':
    manager = ConfigManager()
    soundvis = SoundVis(file=manager.file_path, 
                        config=manager.config)
    graphics = Graphics(file=manager.file_path,
                        data=soundvis.f_hats,
                        config=manager.config)
    graphics.start()
