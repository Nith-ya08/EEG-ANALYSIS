import os
import numpy as np


class Magnitude:
    """
    Job: Take magnitudes of Complex data
    """

    def get_name(self):
        return "mag"

    def apply(self, data):
        return np.absolute(data)


class Log10:
    """
    Apply Log10
    """

    def get_name(self):
        return "log10"

    def apply(self, data):
        data[data <= 0] = np.finfo(float).eps
        return np.log10(data)


def process_data(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    magnitude_operator = Magnitude()
    log10_operator = Log10()

    for filename in os.listdir(input_folder):
        if filename.endswith('.npy'):
            filepath = os.path.join(input_folder, filename)
            data = np.load(filepath)

            magnitude_data = magnitude_operator.apply(data)

            log_data = log10_operator.apply(magnitude_data)

            output_filepath = os.path.join(output_folder, filename)
            np.save(output_filepath, log_data)


input_folder_seizure = r"C:\Users\nithy\Desktop\EEG analysis\rfft_seizure_stack"
output_folder_seizure = r"C:\Users\nithy\Desktop\EEG analysis\transformed_rfft_seizure"
input_folder_non_seizure = r"C:\Users\nithy\Desktop\EEG analysis\rfft_non_seizure_stack"
output_folder_non_seizure = r"C:\Users\nithy\Desktop\EEG analysis\transformed_rfft_non_seizure"

process_data(input_folder_seizure, output_folder_seizure)
process_data(input_folder_non_seizure, output_folder_non_seizure)
