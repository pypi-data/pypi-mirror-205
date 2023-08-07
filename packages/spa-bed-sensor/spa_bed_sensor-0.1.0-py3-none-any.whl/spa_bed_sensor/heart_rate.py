import low_pass_filter as lpf
import numpy as np
from scipy import signal


SLIDE = 500


def smooth(y, box_pts):
    box = np.ones(box_pts) / box_pts
    y_smooth = np.convolve(y, box, mode="same")
    return y_smooth


def heart_rate_estimation(input: list, slide: int = SLIDE, filterorder: int = 6) -> list:
    # Compute the BTB function
    # Input: None
    # Output: BTB function
    # Path: computebtbfunction.py
    flipped_first_half = np.flip(input[:slide])
    input_with_padding = np.concatenate((flipped_first_half, input))
    output_with_padding = lpf.butter_lowpass_filter(input_with_padding, filterorder)
    output = output_with_padding[slide:]

    window_size = 30
    step = 1

    energy_list = []

    for i in range(0, len(output) - window_size + 1, step):
        energy_list.append(sum(output[i : i + window_size] ** 2))

    energy_list = np.array(energy_list)

    output_smooth = smooth(energy_list, 50)

    peaks_idxs = signal.find_peaks(output_smooth)[0]

    temp_out = energy_list
    loc = []
    pks = []

    for i in range(len(peaks_idxs)):
        peak_value = peaks_idxs[i]
        if peak_value < 20:
            tmp_array = temp_out[peak_value : peak_value + 30]
            max_value = max(tmp_array)
            max_index = np.argmax(tmp_array)
            loc.append(peak_value + max_index)
        elif peak_value > len(temp_out) - 30:
            tmp_array = temp_out[peak_value - 20 : peak_value]
            max_value = max(tmp_array)
            max_index = np.argmax(tmp_array)
            loc.append(peak_value - 21 + max_index)
        else:
            tmp_array = temp_out[peak_value - 19 : peak_value + 30]
            max_value = max(tmp_array)
            max_index = np.argmax(tmp_array)

            loc.append(peak_value - 20 + max_index)
        pks.append(max_value)

    peaks_idxs = loc
    temp_out = input
    loc_new = []
    pksn = []

    for i in range(len(peaks_idxs)):
        peak_value = peaks_idxs[i]
        if peak_value < 40:
            tmp_array = temp_out[peak_value : peak_value + 30]
            max_value = max(tmp_array)
            max_index = np.argmax(tmp_array)
            loc_new.append(peak_value + max_index)
        elif peak_value > len(energy_list) - 40:
            tmp_array = temp_out[peak_value - 40 : peak_value]
            max_value = max(tmp_array)
            max_index = np.argmax(tmp_array)
            loc_new.append(peak_value - 41 + max_index)
        else:
            tmp_array = temp_out[peak_value - 39 : peak_value + 30]
            max_value = max(tmp_array)
            max_index = np.argmax(tmp_array)
            loc_new.append(peak_value - 40 + max_index)
        pksn.append(max_value)

    difference = np.diff(loc_new)
    remove_id = np.where(difference == 0)

    loc_new = np.delete(loc_new, remove_id)
    pksn = np.delete(pksn, remove_id)

    numerator = 100 / np.diff(loc_new)

    b2bhrfinal = numerator * 60

    return b2bhrfinal

