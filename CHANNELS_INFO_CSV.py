import pyedflib
import csv
import os

def extract_channels_from_edf(edf_file_path):
    f = pyedflib.EdfReader(edf_file_path)
    n_channels = f.signals_in_file
    channel_labels = f.getSignalLabels()
    f.close()
    return n_channels, channel_labels

def process_edf_files_in_folder(folder_path, csv_file_path):
    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["File Name", "Number of Channels", "Channel Names"])

        for filename in os.listdir(folder_path):
            if filename.endswith(".edf"):
                edf_file_path = os.path.join(folder_path, filename)
                n_channels, channel_labels = extract_channels_from_edf(edf_file_path)
                writer.writerow([filename, n_channels, ', '.join(channel_labels)])

    print(f"Processed EDF files in {folder_path}. Channel information saved to {csv_file_path}")
folder_path = r"C:\Users\nithy\Desktop\EEG analysis\EDFbrowser"
csv_file_path = r"C:\Users\nithy\Desktop\EEG analysis\EDFbrowser\channel_info.csv"
process_edf_files_in_folder(folder_path, csv_file_path)
