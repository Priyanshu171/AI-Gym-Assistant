import tkinter as tk
import os
from subprocess import call

def run_pose_detection():
    selected_pose = var.get()

    if selected_pose == "Squats":
        # Run Squats pose detection code
        print("Running Squats pose detection...")
        call(["python","Squats.py"])

    elif selected_pose == "PullUps":
        # Pull Ups pose detection code
        print("Running Pull Ups pose detection...")
        call(["python", "PullUps.py"])

    elif selected_pose == "Bicep Curls":
        # Run Bicep Curls pose detection code
        print("Running Bicep Curls pose detection...")
        call(["python", "BicepCurl.py"])

    elif selected_pose == "Push Ups":
        # Run Push Ups pose detection code
        print("Running Push Ups pose detection...")
        call(["python", "PushUps.py"])

    elif selected_pose == "Lunges":
        # Lunges pose detection code
        print("Running Lunges pose detection...")
        call(["python", "Lunges.py"])

    elif selected_pose == "Bench Press":
        # Bench Press pose detection code
        print("Running Bench Press pose detection...")
        call(["python", "BenchPress.py"])

    elif selected_pose == "Free Workout":
        # Free Workout pose detection code
        print("Running Free Workout pose detection...")
        call(["python", "free_workout2.py"])


# Create the main window
window = tk.Tk()
window.title("Pose Detection GUI")

# Create a label
label = tk.Label(window, text="Select a Exercise:", font=("Arial", 16))
label.pack(pady=10)

# Create a variable to store the selected pose
var = tk.StringVar(value="")

# Create radio buttons for each pose
poses = ["Lunges","Squats", "PullUps", "Bicep Curls", "Push Ups","Bench Press","Free Workout"]
for pose in poses:
    rb = tk.Radiobutton(window, text=pose, variable=var, value=pose, font=("Arial", 12))
    rb.pack(anchor=tk.W, padx=20, pady=5)

# Create a button to run pose detection
btn = tk.Button(window, text="Run Exercise", command=run_pose_detection, font=("Arial", 14))
btn.pack(pady=20)

# Set window size and center it
window.geometry("500x400")
window.eval('tk::PlaceWindow . center')

# Run the main event loop
window.mainloop()

if __name__ == '__main__':
    # Code that should not be executed when importing
    pass
