import os
import numpy as np
import pyedflib

def read_edf_file(file_path):
    with pyedflib.EdfReader(file_path) as f:
        n_channels = f.signals_in_file
        signal_labels = f.getSignalLabels()
        sigbufs = np.zeros((n_channels, f.getNSamples()[0]))

        for i in np.arange(n_channels):
            sigbufs[i, :] = f.readSignal(i)

    return sigbufs

def process_edf_files(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for file_name in os.listdir(input_folder):
        if file_name.endswith('.edf'):
            file_path = os.path.join(input_folder, file_name)
            matrix = read_edf_file(file_path)
            output_file_path = os.path.join(output_folder, file_name.replace('.edf', '.npy'))
            np.save(output_file_path, matrix)

def main(seizure_folder, non_seizure_folder, output_seizure_folder, output_non_seizure_folder):
    process_edf_files(seizure_folder, output_seizure_folder)
    process_edf_files(non_seizure_folder, output_non_seizure_folder)

if __name__ == "__main__":
    seizure_folder = r"C:\Users\nithy\Desktop\EEG analysis\COMMON_CHANNELS_SEIZURE"
    output_seizure_folder = r"C:\Users\nithy\Desktop\EEG analysis\npy_seizures"

    non_seizure_folder = r"C:\Users\nithy\Desktop\EEG analysis\COMMON_CHANNELS_NON_SEIZURE"
    output_non_seizure_folder = r"C:\Users\nithy\Desktop\EEG analysis\npy_non_seizures"
    main(seizure_folder, non_seizure_folder, output_seizure_folder, output_non_seizure_folder)
