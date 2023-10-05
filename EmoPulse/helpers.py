import numpy as np
from scipy.signal import find_peaks, detrend, butter, filtfilt
from scipy.fftpack import fft, fftfreq

class HeartMetricsCalculator:

    def __init__(self, fps=30, window_length_multiplier=2, step_size_multiplier=1):
        self.fps = fps
        self.window_length = fps * window_length_multiplier
        self.step_size = fps * step_size_multiplier

    @staticmethod
    def bandpass_filter(data, lowcut, highcut, fs, order=5):
        nyquist = 0.5 * fs
        low = lowcut / nyquist
        high = highcut / nyquist
        b, a = butter(order, [low, high], btype='band')
        return filtfilt(b, a, data)

    @staticmethod
    def calculate_heart_rate(peaks, fs):
        time_diff = np.diff(peaks) / fs
        heart_rates = 60 / time_diff
        return np.mean(heart_rates)

    @staticmethod
    def moving_average(data, window_size):
        return np.convolve(data, np.ones(window_size)/window_size, mode='valid')

    @staticmethod
    def compute_IBI(peaks, fs):
        return np.diff(peaks) / fs

    def estimate_heart_rate(self, roi_frames):
        heart_rates = []
        if len(roi_frames) <= 2:
            return 0, 0, 0, 0, 0

        intensity_over_time = [np.mean(frame) for frame in roi_frames]
        detrended_intensity = detrend(intensity_over_time)
        filtered_signal = self.bandpass_filter(detrended_intensity, 0.5, 3, self.fps)

        window_size = int(self.fps/3.0)
        smoothed_signal = self.moving_average(filtered_signal, window_size)

        for start in range(0, len(smoothed_signal) - self.window_length, self.step_size):
            segment = filtered_signal[start:start+self.window_length]
            peaks, _ = find_peaks(segment, distance=self.fps/3.0, height=np.max(segment)*0.6)

            if len(peaks) > 1:
                heart_rate = self.calculate_heart_rate(peaks, self.fps)
                heart_rates.append(heart_rate)

        if len(heart_rates) > 0:
            avg_heart_rate = sum(heart_rates) / len(heart_rates)
        else:
            avg_heart_rate = 0
        
        all_peaks = find_peaks(filtered_signal, distance=self.fps/3.0)[0]
        ibi = self.compute_IBI(all_peaks, self.fps)
        sdnn = np.std(ibi)
        rmssd = np.sqrt(np.mean(np.square(np.diff(ibi))))
        bsi = 1 / rmssd

        frequencies = fftfreq(len(ibi), d=np.mean(ibi))
        power_spectrum = np.abs(fft(ibi))**2
        lf_band = (0.04, 0.15)
        hf_band = (0.15, 0.4)
        lf_power = np.sum(power_spectrum[(frequencies >= lf_band[0]) & (frequencies < lf_band[1])])
        hf_power = np.sum(power_spectrum[(frequencies >= hf_band[0]) & (frequencies < hf_band[1])])
        lf_hf_ratio = lf_power / hf_power

        return avg_heart_rate, sdnn, rmssd, bsi, lf_hf_ratio
