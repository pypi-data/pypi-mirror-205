from scipy import signal


def butter_lowpass_filter(data, filterorder):
    
    # fs is 1Hz which is 100 samples/sec after hardware filtering
    # When using 4th order filtfilt, give filterorder = 2 because filtfilt applies a digital filter forward and backward to a signal. So give value 2 to 4th order.
    b, a = signal.butter(filterorder, [0.014, 0.2], btype="bandpass")
    y = signal.lfilter(b, a, data)

    return y
