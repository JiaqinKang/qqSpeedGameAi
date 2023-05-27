import cv2
import numpy as np
import pyautogui
import time
import json
import pygetwindow as gw
import win32api
import win32con

# Set the desired output video file name
output_file = 'gameplay_capture.mp4'

# Find the QQ Speed window
window_name = 'QQ飞车'
qq_speed_window = gw.getWindowsWithTitle(window_name)[0]

# Get the window coordinates and dimensions
x, y, width, height = qq_speed_window.left, qq_speed_window.top, qq_speed_window.width, qq_speed_window.height
capture_area = (x, y, width, height)

# Define the codec for video output
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
fps = 30.0
frame_period = 1.0 / fps

video_out = cv2.VideoWriter(output_file, fourcc, fps, (int(width), int(height)))

# List of keys that we want to track
tracked_keys = {
    'up': win32con.VK_UP,
    'left': win32con.VK_LEFT,
    'right': win32con.VK_RIGHT
}

# Dictionary to store the state of each key
key_states = {key: {'state': 0, 'hold_duration': 0.0} for key in tracked_keys.keys()}

# Collect frames and key states
data = []
frame_count = 0

while True:
    frame_start_time = time.time()

    # Update key states using win32api
    for key, vk_code in tracked_keys.items():
        if win32api.GetAsyncKeyState(vk_code) != 0:
            if key_states[key]['state'] == 0:
                key_states[key]['state'] = 1
                key_states[key]['hold_duration'] = 0.0
            else:
                key_states[key]['hold_duration'] += frame_period
        else:
            if key_states[key]['state'] == 1:
                key_states[key]['state'] = 0
                key_states[key]['hold_duration'] = 0.0
            

    screenshot = pyautogui.screenshot(region=capture_area)
    frame = np.array(screenshot)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    video_out.write(frame)

    current_key_states = {key: dict(state=value['state'], hold_duration=value['hold_duration']) for key, value in key_states.items()}

    data.append({'frame': frame_count, 'keys': current_key_states})

    frame_count += 1
    frame_end_time = time.time()
    processing_time = frame_end_time - frame_start_time

    sleep_time = frame_period - processing_time
    if sleep_time > 0:
        time.sleep(sleep_time)

    if win32api.GetAsyncKeyState(ord('P')) != 0:
        with open('controls.json', 'w') as f:
            json.dump(data, f, indent=4)

        video_out.release()
        cv2.destroyAllWindows()

        break
