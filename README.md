# Sound Visualizer
Visualize the frequency spectrum of any soundtrack (mp3 or wav) live, and customize the visuals.

## Usage
Run `main.py` with the optional flags `--file <sound file>` and `config <toml file>`:

```powershell
# try example soundfile
python main.py

# specify sound file
python main.py --file <FILE_PATH>

# custom settings
python main.py --file <FILE_PATH> --config <CONFIG_PATH>
```

## Dependencies
OBS! Librosa's read method does not work with numpy 2.0 for mp3 files! If you want to use a mp3 file, either downgrade numpy or convert the file to .wav.

 - numpy (not 2.0 or newer)
 - scipy
 - matplotlib
 - pygame
 - librosa