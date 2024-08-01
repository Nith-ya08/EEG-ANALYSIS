import os
import pyedflib
import numpy as np
import pandas as pd

def extract_seizure_segments(data_path, edf_file, seizure_start_time, seizure_end_time):
    file_path = os.path.join(data_path, edf_file)

    try:
        f = pyedflib.EdfReader(file_path)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return None, None, None
    sfreq = f.getSampleFrequency(0)
    print(sfreq)
    start_sample = int(seizure_start_time * sfreq)
    end_sample = int(seizure_end_time * sfreq)
    seizure_data = []
    for i in range(f.signals_in_file):
        signal = f.readSignal(i)[start_sample:end_sample]
        seizure_data.append(signal)
    f.close()
    seizure_data = np.array(seizure_data)

    return seizure_data, sfreq, f

def save_as_edf(seizure_data, sfreq, f, output_file):
    n_channels = seizure_data.shape[0]
    signal_headers = f.getSignalHeaders()

    edf_writer = pyedflib.EdfWriter(output_file, n_channels, file_type=pyedflib.FILETYPE_EDFPLUS)

    for i in range(n_channels):
        min_value = seizure_data[i].min()
        max_value = seizure_data[i].max()

        if min_value == max_value:
            max_value += 1.0

        signal_headers[i]['physical_min'] = min_value
        signal_headers[i]['physical_max'] = max_value
        signal_headers[i]['digital_min'] = -32768
        signal_headers[i]['digital_max'] = 32767
        signal_headers[i]['sample_frequency'] = sfreq

    edf_writer.setSignalHeaders(signal_headers)
    edf_writer.setPatientCode(f.getPatientCode())
    edf_writer.setPatientName(f.getPatientName())
    edf_writer.setStartdatetime(f.getStartdatetime())

    edf_writer.writeSamples(seizure_data)
    edf_writer.close()
csv_file_path = r"C:\Users\nithy\Desktop\EEG analysis\output.csv"
csv_data = pd.read_csv(csv_file_path)
base_data_path = r"C:\Users\nithy\Desktop\physionet.org\files\chbmit\1.0.0"
output_dir = r"C:\Users\nithy\Desktop\SEIZURE COMPLETE EXTRACTION"
os.makedirs(output_dir, exist_ok=True)

for i in range(1, 25):
    folder_name = f'chb{str(i).zfill(2)}'
    folder_path = os.path.join(base_data_path, folder_name)

    for index, row in csv_data.iterrows():
        edf_file = row['File Name']
        if edf_file.startswith(folder_name):
            num_seizures = row['Number of Seizures']
            seizure_times = row['Seizure Times']


            if num_seizures > 0 and pd.notna(seizure_times):
                seizure_times = seizure_times.strip('()').replace(' ', '').split('),(')
                for j, seizure_time in enumerate(seizure_times):
                    times = seizure_time.split(',')
                    if len(times) == 2:
                        start_time_str, end_time_str = times

                        start_time_parts = start_time_str.split(':')
                        end_time_parts = end_time_str.split(':')

                        seizure_start_time = int(start_time_parts[0]) * 3600 + int(start_time_parts[1]) * 60 + int(
                            start_time_parts[2])
                        seizure_end_time = int(end_time_parts[0]) * 3600 + int(end_time_parts[1]) * 60 + int(
                            end_time_parts[2])

                        print(
                            f"Processing seizure {j + 1} from {seizure_start_time} to {seizure_end_time} in file {edf_file}")


                        seizure_data, sfreq, f = extract_seizure_segments(folder_path, edf_file, seizure_start_time,
                                                                          seizure_end_time)

                        if seizure_data is not None:

                            output_file = os.path.join(output_dir,
                                                       f"{edf_file.replace('.edf', '')}_seizure_{j + 1}.edf")
                            save_as_edf(seizure_data, sfreq, f, output_file)
                            print(f"Seizure segment saved as {output_file}")
                        else:
                            print(f"Failed to extract seizure segment from {edf_file}")
                    else:
                        print(f"Unexpected seizure time format: {seizure_time}")

print("Processing complete.")
