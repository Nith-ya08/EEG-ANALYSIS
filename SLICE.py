import os
import numpy as np


class Slice:
    """
    Job: Take a slice of the data on the last axis.
    Note: Slice(x, y) works like a normal python slice, that is x to (y-1) will be taken.
    """

    def __init__(self, start, stop):
        self.start = start
        self.stop = stop + 1

    def get_name(self):
        return "slice%d-%d" % (self.start, self.stop)

    def apply(self, data):
        return data[..., self.start:self.stop]


def stack_data(input_folder, output_folder, slice_size):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith('.npy'):
            filepath = os.path.join(input_folder, filename)
            data = np.load(filepath)
            num_slices = data.shape[-1] // slice_size
            stacked_data = np.stack([data[..., i * slice_size:(i + 1) * slice_size] for i in range(num_slices)], axis=0)

            output_filepath = os.path.join(output_folder, filename)
            np.save(output_filepath, stacked_data)

input_folder_seizure = r"C:\Users\nithy\Desktop\EEG analysis\npy_seizures"
output_folder_seizure = r"C:\Users\nithy\Desktop\EEG analysis\stack_seizures"
input_folder_non_seizure = r"C:\Users\nithy\Desktop\EEG analysis\npy_non_seizures"
output_folder_non_seizure = r"C:\Users\nithy\Desktop\EEG analysis\stack_non_seizures"

slice_size = 256

stack_data(input_folder_seizure, output_folder_seizure, slice_size)
stack_data(input_folder_non_seizure, output_folder_non_seizure, slice_size)
