from GUI import run_pose_estimation

max_freq_element = 2

classes=["Push Ups","Pulls Ups","Squats"]
run_pose_estimation(classes[max_freq_element])
print("Predicted class:", classes[max_freq_element])