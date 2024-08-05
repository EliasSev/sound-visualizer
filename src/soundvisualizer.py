import scipy as sp
import numpy as np
import librosa as lr


class SoundVis:
    def __init__(self, file, fps, span, s_width, scaling, smoothing=0, nsmooth=1, stop=None, time_smoothing=3):
        """
        file, str      : name of .wav (or .mp3) file
        fps, int       : frames per second
        span, tuple    : frequency range in Hz
        s_width, float : length of audio slices (s)
        scaling, float : scale down dominating frequencies (0 to 1)
        smooth, int    : number of points in convolution
        nsmooth, int   : number of interations to apply smoothing
        stop, float    : stopping time of audio in seconds
        """
        
        # Avoid librosa if possible: numpy>=2.0.0 incompatiable with librosa.load
        audio_format = file.split('.')[-1]
        if audio_format == "wav":
            wav = sp.io.wavfile.read(file)
            self.fs = wav[0]  # sampling rate
            self.f = wav[1]   # signal
        elif audio_format == "mp3":
            mp3 = lr.load(file, sr=None, duration=stop)
            self.fs = mp3[1]
            self.f = mp3[0]
        else:
            raise ValueError("Unknown audio type:", audio_format)

        # if stereo
        if len(self.f.shape) == 2:
            self.f = self.f[:, 0]
        
        self.fps = fps
        self.N = self.f.size  # data points
        self.T = self.N / self.fs  # time in seconds
        self.span = span
        self.f_hats = self.f_hat_slices(s_width, scaling)

        # smoothing (convolution)
        if smoothing != 0:
           for _ in range(nsmooth):
            self.convolution(smoothing)

        if time_smoothing != 0:
            self.time_smooth(time_smoothing)


    def _normalize(self, data):
        m = max([max(y) for y in data])
        return [y / m for y in data]
    

    def f_hat_slices(self, width, scaling):
        """
        Construct the frequency slices (absolute value).
        width, float : width of a souns slice
        """

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

        return self._normalize(f_hats)
    

    def convolution(self, box_pts):
        """
        y, list      : data to be smoothed
        box_pts, int : width of box to use in convolution
        """
        box = np.ones(box_pts) / box_pts
        f_smooth = [np.convolve(yi, box, mode='same') for yi in self.f_hats]
        self.f_hats = self._normalize(f_smooth)


    def time_smooth(self, n):
        """
        Average out the current frame with the n last frames, with weights 1/2, 1/3, ..., 1/n.
        n, int : number of previous frames to smooth with
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
