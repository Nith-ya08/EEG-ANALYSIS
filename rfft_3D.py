import os
import numpy as np


def perform_fft(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith('.npy'):
            filepath = os.path.join(input_folder, filename)
            data = np.load(filepath)

            fft_data = np.fft.rfft(data, axis=-1)

            output_filepath = os.path.join(output_folder, filename)
            np.save(output_filepath, fft_data)

input_folder_seizure = r"C:\Users\nithy\Desktop\EEG analysis\stack_seizures"
output_folder_seizure = r"C:\Users\nithy\Desktop\EEG analysis\rfft_seizure_stack"
input_folder_non_seizure = r"C:\Users\nithy\Desktop\EEG analysis\stack_non_seizures"
output_folder_non_seizure = r"C:\Users\nithy\Desktop\EEG analysis\rfft_non_seizure_stack"

perform_fft(input_folder_seizure, output_folder_seizure)
perform_fft(input_folder_non_seizure, output_folder_non_seizure)
