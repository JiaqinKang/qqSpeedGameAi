import cv2
import csv
import json
import numpy as np
import random

# Define the preprocess_frame function according to your requirements
def preprocess_frame(frame):
    # randomly flip the image at random angle, crop the image but obtain the same size to keep original 640x480, inverse the color randomly
    # if statement to handle random decision
    numbers = [1, 2, 3, 4, 5]
    random_number = random.choice(numbers)

    if random_number == 2:  # crop the image but obtain the same size to keep original 640x480
        processed_frame = frame[0:480, 0:640]
    elif random_number == 3:  # inverse the color randomly with random color
        processed_frame = cv2.bitwise_not(frame)
        processed_frame = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2HSV)
        processed_frame[:, :, 0] = (processed_frame[:, :, 0] + random.randint(0, 255)) % 255
        processed_frame = cv2.cvtColor(processed_frame, cv2.COLOR_HSV2BGR)
    elif random_number == 4:  # filter on depth
        processed_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        processed_frame[:, :, 0] = (processed_frame[:, :, 0] + random.randint(0, 255)) % 255
        processed_frame = cv2.cvtColor(processed_frame, cv2.COLOR_HSV2BGR)
    else:  # original image
        processed_frame = frame

    # resize the image to 320x240
    processed_frame = cv2.resize(processed_frame, (320, 240))

    return processed_frame

# Define the preprocess_key_states function according to your requirements
def preprocess_key_states(key_states):
    # Placeholder function for key states preprocessing
    # Implement your own preprocessing steps here
    processed_key_states = {
        'up_state': key_states['up']['state'],
        'up_hold_duration': key_states['up']['hold_duration'],
        'left_state': key_states['left']['state'],
        'left_hold_duration': key_states['left']['hold_duration'],
        'right_state': key_states['right']['state'],
        'right_hold_duration': key_states['right']['hold_duration'],
    }

    return processed_key_states

# Load controls.json
with open('controls.json', 'r') as f:
    controls_data = json.load(f)

# Load gameplay video
video_path = 'gameplay_capture.mp4'
cap = cv2.VideoCapture(video_path)

# Create CSV file for the dataset
csv_file = 'dataset.csv'
csv_headers = [
    'frame_path',
    'up_state', 'up_hold_duration',
    'left_state', 'left_hold_duration',
    'right_state', 'right_hold_duration',
]
with open(csv_file, 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=csv_headers)
    writer.writeheader()

    # Iterate over frames and key states
    frame_idx = 0
    while cap.isOpened() and frame_idx < len(controls_data):
        ret, frame = cap.read()
        if not ret:
            break

        # Check if the current frame index exists in controls_data
        if frame_idx >= len(controls_data):
            break

        # Get the frame object from controls_data
        frame_obj = controls_data[frame_idx]

        # Get the frame number from the frame object
        frame_num = frame_obj['frame']

        # Check if the current frame number matches the frame index
        if frame_num == frame_idx:
            # Preprocess frame (e.g., resize, normalize, augment)
            processed_frame = preprocess_frame(frame)

            # Get key states for the current frame
            key_states = frame_obj['keys']

            # Preprocess key states (e.g., encode into numerical labels or one-hot encoding)
            processed_key_states = preprocess_key_states(key_states)

            # Save frame image as a separate file (optional) and size down to original /2
            frame_filename = f'frames/frame_{frame_idx}.jpg'
            cv2.imwrite(frame_filename, processed_frame)

            # Save frame path and key states in the CSV row
            csv_row = {'frame_path': frame_filename, **processed_key_states}
            writer.writerow(csv_row)

            frame_idx += 1
            print(f'Processed frame {frame_idx}')
        else:
            # If the current frame number doesn't match the frame index,
            # continue to the next frame in the video
            continue

cap.release()
