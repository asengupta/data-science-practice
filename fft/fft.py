import math
from functools import reduce

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from scipy.fft import rfft, rfftfreq
from scipy.signal import periodogram

DEFAULT_DATASET_LOCATION = "~/Downloads"
DEFAULT_DATA_CSV_FILENAME = "ecg1.csv"


def study(raw_data):
    ecg_data = raw_data['0'].values
    yf = rfft(ecg_data)
    plt.figure()
    plt.title("Raw ECG Series")
    plt.plot(ecg_data)
    plt.show()

    total_time = 30
    threshold = 600

    sampling_frequency = len(ecg_data) / total_time
    sample_spacing = 1.0 / sampling_frequency
    num_sample_points = len(ecg_data)
    xf = rfftfreq(num_sample_points, sample_spacing)[:int(num_sample_points // 2)]
    plt.figure()
    plt.title("Frequency Domain (Log Normalised)")
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('Amplitude (log 10)')
    yf = np.log10(2.0 / num_sample_points * np.abs(yf[:int(num_sample_points // 2)]))
    plt.plot(xf, yf)
    plt.grid()
    plt.show()

    f, power_density = periodogram(ecg_data, fs=sampling_frequency)
    plt.figure()
    plt.title("Power Spectral Density")
    plt.plot(f[:13], 1000 * (power_density[:13]))
    plt.ylim([1e-7, 4000])
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('PSD [V^2*1000/Hz]')
    plt.grid()
    plt.show()

    print(f"LF Band Power={bandpower(ecg_data, sampling_frequency, 0.04, 0.15)} W")
    print(f"HF Band Power={bandpower(ecg_data, sampling_frequency, 0.15, 0.4)} W")
    print(f"RMSSD = {rmssd(ecg_data, threshold, total_time)}")


def bandpower(x, fs, fmin, fmax):
    f, Pxx = periodogram(x, fs=fs)
    ind_min = np.argmax(f > fmin) - 1
    ind_max = np.argmax(f > fmax) - 1
    return np.trapz(Pxx[ind_min: ind_max], f[ind_min: ind_max])


def rmssd(x, threshold, total_time_in_seconds):
    peaks = x
    ticks = []
    tick = 0
    for index, peak in enumerate(peaks):
        if peak > threshold:
            ticks.append(tick)
            tick = 0
        else:
            tick += 1
    ticks = ticks[1:-1]
    tick_duration = total_time_in_seconds / len(x)
    rr_intervals = map(lambda tick_count: tick_count * tick_duration, ticks)
    squared_rr_intervals = map(lambda rr: rr * rr, rr_intervals)
    rms_rr_intervals = math.sqrt(reduce(lambda x, y: x + y, squared_rr_intervals, 0) / len(ticks))
    return rms_rr_intervals


def read_csv(csv):
    return pd.read_csv(csv, low_memory=False)


def main():
    study(read_csv(f"{DEFAULT_DATASET_LOCATION}/{DEFAULT_DATA_CSV_FILENAME}"))


main()
