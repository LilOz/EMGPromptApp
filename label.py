import os
import pandas as pd

def label_emg_df(emg_df, label_df, filename=None):

    try:
        # Filter EMG data to start from the first timestamp in label_df
        min_label_time = label_df['time_unix'].min()
        max_label_time = label_df['time_unix'].max()
        emg_df = emg_df[(emg_df[' Timestamp'] >= min_label_time) & (emg_df[' Timestamp'] <= max_label_time)].copy()

        # Assign labels by finding the closest timestamp in label_df for each EMG row
        emg_df['class'] = emg_df[' Timestamp'].apply(lambda t: label_df.loc[(label_df['time_unix'] - t).abs().idxmin(), 'class'])
    
    except Exception as e:
        print("Error (Probably a folder not intended for merging)", e)

    # Save the labeled DataFrame
    emg_df.to_csv((filename or 'emg_labeled') + ".txt", index=False)
    print(f"Labeled EMG data saved to {(filename or 'emg_labeled') + '.txt'}")


def auto_detect_files_in_subfolders():
    # Walk through all subdirectories and files in the current directory
    for root, _, files in os.walk('./Output Files'):
        emg_file = None
        label_file = None

        for file in files:
            if file.endswith('.txt'):  # EMG file heuristic
                emg_file = os.path.join(root, file)
            elif file.endswith('.csv'):  # Label file heuristic
                label_file = os.path.join(root, file)

        if emg_file and label_file:
            # Load the EMG and label data
            emg_df = pd.read_csv(emg_file, comment='%', skiprows=1)  # Adjust if needed
            label_df = pd.read_csv(label_file)

            # Create the output filename for the labeled data in the same directory
            output_filename = os.path.join(root, "labeled_emg_output")

            # Call the function to label the EMG data
            label_emg_df(emg_df, label_df, filename=output_filename)
        else:
            print(f"Required EMG and label files not found in directory: {root}")

# Run the function to process all subfolders
auto_detect_files_in_subfolders()
