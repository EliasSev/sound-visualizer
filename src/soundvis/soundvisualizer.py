import scipy as sp
import numpy as np
import librosa as lr


class SoundVis:
    """
    A class to process and visualize the frequency spectrum of audio files.

    This class reads an audio file, processes its frequency spectrum over
    defined time windows, and allows for various smoothing techniques.

    Parameters
    ----------
    file : str
        Path to the audio file to be processed.
    fps : int
        Frames per second for the analysis.
    processing : dict
        A dictionary containing processing parameters:
        - 'window': float, width of the time window (in seconds).
        - 'scaling': float, scaling factor for suppressing dominant frequencies.
        - 'smoothing': int, width of the smoothing kernel for convolution.
        - 'n-smooth': int, number of smoothing iterations.
        - 'span': tuple, range of frequencies to include (start, stop).
        - 'time-smoothing': int, number of frames to smooth temporally.
        - 'stop': float, duration (in seconds) to process the audio.
    """

    def __init__(self, file, fps, processing):
        if not isinstance(file, str):
            assert ValueError(f"'file' must be of type str, not {type(file).__name__}")
        if not isinstance(fps, int):
            assert ValueError(f"'fps' must be of type int, not {type(fps).__name__}")
        if not isinstance(processing, str):
            assert ValueError(f"'processing' must be of type dict, not {type(processing).__name__}")

        window_size = processing['window']
        scaling = processing['scaling']
        smoothing = processing['smoothing']
        n_smooth = processing['n-smooth']
        span = processing['span-hz']
        time_smoothing = processing['time-smoothing']
        stop = processing['stop-time']

        self.f, self.fs = self._read_audio(file, stop)
        self.fps = fps
        self.N = self.f.size  # data points
        self.T = self.N / self.fs  # time in seconds
        self.span = span
        self.f_hats = self.f_hat_slices(window_size, scaling)

        # smoothing (convolution)
        if smoothing != 0:
           for _ in range(n_smooth):
            self.convolution(smoothing)

        if time_smoothing != 0:
            self.time_smooth(time_smoothing)

    @staticmethod
    def _read_audio(file, stop):
        """
        Read an audio file and return the signal and sampling rate.

        Parameters
        ----------
        file : str
            Path to the audio file.
        stop : float
            Duration to stop reading the audio file.

        Returns
        -------
        f : numpy.ndarray
            The audio signal.
        fs : int
            The sampling rate of the audio signal.
        """
        # Avoid librosa if possible: numpy>=2.0.0 incompatiable with librosa.load
        audio_format = file.split('.')[-1]
        if audio_format == "wav":
            wav = sp.io.wavfile.read(file)
            fs = wav[0]  # sampling rate
            f = wav[1]   # signal
        elif audio_format == "mp3":
            mp3 = lr.load(file, sr=None, duration=stop)
            fs = mp3[1]
            f = mp3[0]
        else:
            raise ValueError("Unknown audio type:", audio_format)
        # if stereo
        if len(f.shape) == 2:
            f = f[:, 0]
        return f, fs

    def _normalize(self, data):
        """
        Normalize the data.

        Parameters
        ----------
        data : list of numpy.ndarray
            List of arrays to normalize.

        Returns
        -------
        list of numpy.ndarray
            Normalized data.
        """
        m = max([max(y) for y in data])
        return [y / m for y in data]
    
    def f_hat_slices(self, width, scaling):
        """
        Construct the frequency slices (absolute value).

        Parameters
        ----------
        width : float
            Width of a sound window.
        scaling : float
            Scaling factor for frequency suppression.

        Returns
        -------
        list of numpy.ndarray
            List of frequency spectra for each frame.
        """

        print("\nProcessing sound file\n" + '-' * 40)
        if type(self.fps) != float or self.fps <= 0:
            assert ValueError("fps must be a positive integer")

        S = int(self.fps * self.T)  # number of slices
        L = int(self.N * width / self.T)  # slice length
        dn = self.N / S  # step size

        f_hats = []
        for i in range(S):
            fi = self.f[int(i * dn) : int(i * dn) + L]  # slice
            Ni = fi.size
            if Ni == 0:
                break
            
            # FFT (absolute value)
            fi_hat = np.abs(np.fft.fft(fi))
        
            # supress dominationg frequencies
            if scaling != 0:
                fi_hat = fi_hat**scaling

            # index of start/stop
            start, stop = self.span[0] * Ni // self.fs, self.span[1] * Ni // self.fs
            f_hats.append(fi_hat[start:stop])
            if not (i + 1 % 25) or (i + 1 == S):
                progress_bar(i + 1, S)

        return self._normalize(f_hats)
    
    def convolution(self, box_pts):
        """
        Apply convolution smoothing to the frequency spectra.

        Parameters
        ----------
        box_pts : int
            Number of points in the convolution box.
        """
        box = np.ones(box_pts) / box_pts
        f_smooth = [np.convolve(yi, box, mode='same') for yi in self.f_hats]
        self.f_hats = self._normalize(f_smooth)

    def time_smooth(self, n):
        """
        Average out the current frame with the n last frames, with weights 1/2, 1/3, ..., 1/n.

        Parameters
        ----------
        n : int
            Number of previous frames to smooth with.
        """
        new_f_hats = []
        Ni = len(self.f_hats[0])
        for i in range(len(self.f_hats)):
            f_hat = self.f_hats[i].copy()

            if i <= n or len(f_hat) != Ni:
                new_f_hats.append(f_hat)
                continue
            
            for j in range(n):
                # weighted average
                f_hat += self.f_hats[i-j-1] / (j + 1)

            new_f_hats.append(f_hat) 
        self.f_hats = self._normalize(new_f_hats)


def progress_bar(step, total_steps, bar_length=30, fill='#', end_text=''):
    """
    Simple progress bar.
    """
    
    filled = int(bar_length * step / total_steps)
    text = f"[{filled * fill :<{bar_length}}] {step}/{total_steps}"
    end = '\r' if step < total_steps else '\n\n' 
    print(text + end_text, end=end)
