import os
import pandas as pd
from datetime import timedelta
folder_path = r"C:\Users\nithy\Desktop\physionet.org\files\chbmit\1.0.0"

def seconds_to_hms(seconds):
    return str(timedelta(seconds=seconds))

def parse_summary_file(file_path):
    data = []
    file_name = None
    start_time = 'NA'
    end_time = 'NA'

    with open(file_path, 'r') as file:
        lines = file.readlines()
        lines_iter = iter(lines)
        for line in lines_iter:
            if line.startswith("File Name:"):
                file_name = line.split(": ")[1].strip()
            elif line.startswith("File Start Time:"):
                start_time = line.split(": ")[1].strip()
            elif line.startswith("File End Time:"):
                end_time = line.split(": ")[1].strip()
            elif line.startswith("Number of Seizures in File:"):
                num_seizures = int(line.split(": ")[1].strip())
                seizures = []
                if num_seizures > 0:
                    for i in range(num_seizures):
                        seizure_start = None
                        seizure_end = None
                        try:
                            line = next(lines_iter).strip()
                            if f"Seizure {i+1} Start Time:" in line or "Seizure Start Time:" in line:
                                seizure_start = int(line.split(": ")[1].strip().split()[0])
                            line = next(lines_iter).strip()
                            if f"Seizure {i+1} End Time:" in line or "Seizure End Time:" in line:
                                seizure_end = int(line.split(": ")[1].strip().split()[0])
                            seizure_start_hms = seconds_to_hms(seizure_start)
                            seizure_end_hms = seconds_to_hms(seizure_end)
                            seizures.append(f"({seizure_start_hms},{seizure_end_hms})")
                        except Exception as e:
                            print(f"Error parsing seizures for file {file_name}: {e}")
                    seizures_str = ",".join(seizures)
                    if file_name:
                        data.append([file_name, start_time, end_time, num_seizures, seizures_str])
                    else:
                        print(f"Warning: Missing file name in file {file_path}")
                else:
                    if file_name:
                        data.append([file_name, start_time, end_time, num_seizures, None])
                    else:
                        print(f"Warning: Missing file name in file {file_path}")

    return data
all_data = []
for i in range(1, 25):
    file_num = str(i).zfill(2)
    file_name = f'chb{file_num}\chb{file_num}-summary.txt'
    file_path = os.path.join(folder_path, file_name)
    if os.path.exists(file_path):
        print(f"Parsing file: {file_path}")
        file_data = parse_summary_file(file_path)
        if file_data:
            print(f"Data parsed from file {file_name}: {file_data}")
        all_data.extend(file_data)
    else:
        print(f"File does not exist: {file_path}")
if all_data:
    df = pd.DataFrame(all_data, columns=['File Name', 'Start Time', 'End Time', 'Number of Seizures', 'Seizure Times'])
    output_csv_path = 'output.csv'
    df.to_csv(output_csv_path, index=False)
    print(f"CSV file saved to {output_csv_path}")
else:
    print("No data parsed. CSV file not created.")
