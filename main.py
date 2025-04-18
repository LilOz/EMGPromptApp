import datetime
import os
import random
import time
import tkinter as tk
from threading import Thread

import pandas as pd
from PIL import Image, ImageTk  # Pillow for image handling

# Define gestures and corresponding image files
gestures = {
    "Hand Rest": "hand_rest.png",
    "Fist": "fist.png",
    "Wrist Flexion": "wrist_flexion.png",
    "Wrist Extension": "wrist_extension.png",
    "Radial Deviation": "radial_deviation.png",
    "Ulnar Deviation": "ulnar_deviation.png",
}

gesture_labels = {
    "Hand Rest": 1,
    "Fist": 2,
    "Wrist Flexion": 3,
    "Wrist Extension": 4,
    "Radial Deviation": 5,
    "Ulnar Deviation": 6,
}


class EMGApp:
    def __init__(self, root):
        self.root = root
        self.root.title("EMG Recording Protocol")
        self.root.geometry("700x700")  # Set a larger window size

        self.gesture_labels = []

        # Default durations and repetitions
        self.default_gesture_duration = 4  # Default: 4 seconds
        self.default_rest_duration = 4  # Default: 4 seconds
        self.default_repetitions = 3  # Default: 3 repetition

        # Initialize UI components
        self.phase_label = tk.Label(
            root, text="Press Start to Begin", font=("Arial", 36), width=30, height=2
        )
        self.phase_label.pack(pady=10)

        # File name and config input fields
        self.config_frame = tk.Frame(root)
        self.config_frame.pack(pady=10)

        self.add_config_input("File Name Prefix:", "file_name_entry", 20, "")
        self.add_config_input(
            "Gesture Duration (s):",
            "gesture_duration_entry",
            5,
            self.default_gesture_duration,
        )
        self.add_config_input(
            "Rest Duration (s):", "rest_duration_entry", 5, self.default_rest_duration
        )
        self.add_config_input(
            "Repetitions:", "repetitions_entry", 5, self.default_repetitions
        )

        self.start_button = tk.Button(
            root,
            text="Start",
            font=("Arial", 28),
            command=self.start_protocol,
            width=10,
        )
        self.start_button.pack(pady=10)

        # Container for next pose label and icon (fixed size)
        self.next_pose_frame = tk.Frame(root, width=600, height=100)  # Fixed size
        self.next_pose_frame.pack_propagate(False)  # Prevent resizing
        self.next_pose_frame.pack(pady=5, expand=True, anchor="center")

        self.next_pose_label = tk.Label(
            self.next_pose_frame, text="", font=("Arial", 24), width=20, anchor="w"
        )
        self.next_pose_label.pack(side="left", padx=10)

        self.next_pose_icon = tk.Label(self.next_pose_frame)  # Label for the small icon
        self.next_pose_icon.pack(side="right", padx=10)

        self.timer_label = tk.Label(root, text="", font=("Arial", 28))
        self.timer_label.pack(pady=10)

        self.image_label = tk.Label(root)  # Label to display pose images
        self.image_label.pack(pady=10)

        self.running = False

    def add_config_input(self, label_text, attr_name, width, default_value):
        """Add configuration input field with default values."""
        frame = tk.Frame(self.config_frame)
        frame.pack(pady=5)

        label = tk.Label(frame, text=label_text, font=("Arial", 14))
        label.pack(side="left", padx=5)

        entry = tk.Entry(frame, font=("Arial", 14), width=width)
        entry.insert(0, str(default_value))  # Set the default value
        setattr(self, attr_name, entry)
        entry.pack(side="left", padx=5)

    def start_protocol(self):
        # Get user inputs
        prefix = self.file_name_entry.get().strip()
        gesture_duration = self.gesture_duration_entry.get().strip()
        rest_duration = self.rest_duration_entry.get().strip()
        repetitions = self.repetitions_entry.get().strip()

        # Validate and set durations and repetitions
        try:
            self.gesture_duration = int(gesture_duration)
            self.rest_duration = int(rest_duration)
            self.repetitions = int(repetitions)
        except ValueError:
            self.update_label("Invalid Input!", color="red")
            return

        # Create file name
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.save_file = f"{prefix}_{timestamp}" if prefix else f"{timestamp}"

        # Hide configuration inputs
        self.config_frame.pack_forget()

        self.running = True
        # self.start_button.config(state="disabled")  # Disable the button while running
        self.start_button.pack_forget()
        protocol_thread = Thread(target=self.run_protocol)
        protocol_thread.start()

    def run_protocol(self):
        self.update_image(gestures["Hand Rest"])
        self.update_label("Get Ready!", color="gray")

        # Prepare gesture order for all repetitions
        gesture_order = random.sample([g for g in gestures.keys()], len(gestures))

        # Show the first pose in the "Next Pose" section during the countdown
        first_pose = gesture_order[0]
        self.update_next_pose(f"Next: {first_pose}", gestures[first_pose])

        # Initial countdown
        self.run_timer(10, "Starting In")

        debug_start_time = 0

        for repitition in range(self.repetitions):
            if not self.running:
                break

            next_gesture_order = random.sample(
                [g for g in gestures.keys()], len(gestures)
            )

            for i, next_pose in enumerate(gesture_order):
                if not self.running:
                    break

                # Perform the gesture
                self.update_image(gestures[next_pose])
                self.update_label(f"Perform: {next_pose}", color="green")
                self.hide_next_pose()  # Hide the "next pose" section

                if debug_start_time != 0:
                    print(f"Rest Took {round(time.time() - debug_start_time, 2)} seconds")
                debug_start_time = time.time()

                pose_start_time = time.time()
                self.run_timer(self.gesture_duration, "Hold Gesture")

                if not self.running:
                    break

                # Show the next pose during the rest phase
                if i < len(gesture_order) - 1:
                    next_next_pose = gesture_order[i + 1]
                else:
                    next_next_pose = next_gesture_order[0]

                if repitition == self.repetitions - 1 and i == len(gesture_order) - 1:
                    self.update_next_pose("", None)
                else:
                    self.update_next_pose(
                        f"Next: {next_next_pose}", gestures[next_next_pose]
                    )

                # Rest phase
                self.update_image(gestures["Hand Rest"])
                self.update_label("Rest", color="red")
                print(
                    f"Perform gesture: {next_pose} Took {round(time.time() - debug_start_time, 2)} seconds"
                )
                debug_start_time = time.time()
                pose_end_time = time.time()
                self.gesture_labels.append((gesture_labels[next_pose], pose_start_time, pose_end_time)) # array of (pose, start_time, end_time)
                print(self.gesture_labels)
                self.run_timer(self.rest_duration, "Rest and wait for next gesture")

            gesture_order = next_gesture_order

        # End protocol
        self.update_label("Complete!", color="gray")
        self.timer_label.config(text="")
        self.update_next_pose("", None)
        self.create_dataframe()
        self.update_image(None)  # Clear the image
        self.start_button.config(state="normal")  # Re-enable the button

        # Re-enable and re-display the configuration options
        self.config_frame.pack(pady=10)
        self.file_name_entry.config(state="normal")
        self.gesture_duration_entry.config(state="normal")
        self.rest_duration_entry.config(state="normal")
        self.repetitions_entry.config(state="normal")

        # Reshow the start button
        self.start_button.pack(pady=10)

    def update_label(self, text, color=None):
        """Update the central label."""
        self.phase_label.config(text=text)
        if color:
            self.phase_label.config(bg=color, fg="white")

    def update_next_pose(self, text, image_path=None):
        """Update the 'next pose' label and icon without resizing the frame."""
        self.next_pose_label.config(text=text)
        if image_path:
            img = Image.open(image_path)
            img = img.resize((150, 150))  # Resize the icon to a smaller size
            photo = ImageTk.PhotoImage(img)
            self.next_pose_icon.config(image=photo)
            self.next_pose_icon.image = (
                photo  # Keep a reference to prevent garbage collection
            )
        else:
            self.next_pose_icon.config(image="")  # Clear the icon

    def hide_next_pose(self):
        """Hide the 'next pose' section during gesture performance."""
        self.next_pose_label.config(text="")
        self.next_pose_icon.config(image="")

    def update_image(self, image_path):
        """Update the main pose image."""
        if image_path:
            img = Image.open(image_path)
            img = img.resize((300, 300))  # Resize the main image to be larger
            photo = ImageTk.PhotoImage(img)
            self.image_label.config(image=photo)
            self.image_label.image = (
                photo  # Keep a reference to prevent garbage collection
            )
        else:
            self.image_label.config(image="")  # Clear the image

    def run_timer(self, duration, action_text):
        """Run the countdown timer."""
        for remaining in range(duration, 0, -1):
            self.timer_label.config(text=f"{action_text}: {remaining}s")
            time.sleep(1)
            if not self.running:
                break

    # def create_dataframe(self):
    #     """Save the gesture labels and timing into a CSV file."""
    #     classes = []
    #     times = []
    #     times_unix = []
    #
    #     time_step = 0.004  # 250 Hz sample rate
    #     time_index = 0
    #
    #     for label in self.gesture_labels:
    #         # Handle adding the class the correct number of times
    #         classes += [label] * 250 * self.gesture_duration
    #         for _ in range(250 * self.gesture_duration):
    #             times_unix.append(time_index * time_step + self.start_time)
    #             times.append(time_index * time_step)
    #             time_index += 1
    #
    #         # Handle the rest period
    #         classes += [0] * 250 * self.rest_duration
    #         for _ in range(250 * self.rest_duration):
    #             times_unix.append(time_index * time_step + self.start_time)
    #             times.append(time_index * time_step)
    #             time_index += 1
    #
    #     data = {"class": classes, "time": times, "time_unix": times_unix}
    #
    #     df = pd.DataFrame(data)
    #     # Ensure the directory exists
    #     os.makedirs("Output Files", exist_ok=True)
    #
    #     # Ensure the directory exists
    #     directory = os.path.join("Output Files", self.save_file)
    #     if not os.path.exists(directory):
    #         os.makedirs(directory)
    #
    #     # Save the CSV file
    #     df.to_csv(os.path.join(directory, "labels.csv"))

    def create_dataframe(self):
        """Save the gesture labels and timing into a CSV file."""
        classes = []
        times = []
        times_unix = []

        time_step = 0.004  # 250 Hz sample rate
        self.start_time = self.gesture_labels[0][1]
        t = 0  

        for label, start_time, end_time in self.gesture_labels:
            # Handle adding the class the correct number of times
            while t + self.start_time < start_time:
                classes.append(0) # rest period
                times_unix.append(t + self.start_time)
                times.append(t) 
                t += time_step

            while t + self.start_time < end_time:
                classes.append(label)
                times_unix.append(t + self.start_time)
                times.append(t)
                t += time_step

        data = {"class": classes, "time": times, "time_unix": times_unix}

        df = pd.DataFrame(data)

        # Ensure the directory exists
        os.makedirs("Output Files", exist_ok=True)

        # Ensure the directory exists
        directory = os.path.join("Output Files", self.save_file)
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Save the CSV file
        df.to_csv(os.path.join(directory, "labels.csv"))
        print(f"Data saved to {os.path.join(directory, "labels.csv")}")

    def stop_protocol(self):
        """Stop the recording protocol."""
        self.running = False


# Run the application
root = tk.Tk()
app = EMGApp(root)
root.mainloop()
