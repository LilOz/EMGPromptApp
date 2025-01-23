# EMG Recording Protocol Application

This application is designed to guide users through a protocol for recording EMG (Electromyography) data. It provides a graphical interface for performing and timing specific hand gestures, saving the results to a CSV file for further analysis (can be easily synced and combined with emg data from cyton).

## Features

- Gesture Timing: Perform and time specific hand gestures with customizable durations.

- Rest Periods: Includes rest periods between gestures.

- Randomized Order: Gestures are randomized for each repetition.

- Data Logging: Saves gesture labels and timing data to a CSV file.

- User-Friendly Interface: Simple and intuitive GUI for ease of use.

## Requirements

- Python 3.7 or higher https://www.python.org/downloads/
- Pillow (for image handling)
- Pandas (for data logging)

# Setup Instructions

### 1. Clone repository and Open the directory in your terminal

```
git clone https://github.com/LilOz/EMGPromptApp
```

```
cd EMGPromptApp
```

### 2. Create a virtual environment:

```
python -m venv venv
```

or

```
python3 -m venv venv
```

### 3. Activate virtual environment:

Windows

```
venv\Scripts\activate
```

MacOS / Linux

```
source venv/bin/activate
```

After doing this you should see (venv) in your terminal

### 4. Install Dependencies:

```
pip install -r requirements.txt
```

# Usage

### 1. Run the Application

```
python main.py
```

### 2. Enter settings

- Enter a file name prefix (optional)
- Set the gesture duration, rest duration, and number of repitions (the defaults work fine)
- Click start

### 3. Output

- The gesture labels and timing data are saved in a CSV file inside the `Output Files` folder.
