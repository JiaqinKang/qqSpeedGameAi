import cv2
import numpy as np
import keras
import pygetwindow as gw
from mss import mss
from pynput.keyboard import Controller, Key
import time
import win32api


# Load model
model = keras.models.load_model('model2.h5')
prev_key_stroke = None
QuitKey = 'Q'
# Find the QQ Speed window
window_name = 'QQ飞车2.0'  # Adjust this if the window name is different
qq_speed_window = gw.getWindowsWithTitle(window_name)[0]

# Mapping of index to key strokes
key_mapping = {
    0: Key.left,
    1: Key.right,
    2: Key.up
}

# Set up the MSS capture
region = {'top': qq_speed_window.top, 'left': qq_speed_window.left, 
          'width': qq_speed_window.width, 'height': qq_speed_window.height}
sct = mss()

# Create a keyboard controller
keyboard = Controller()

# Main loop to capture and display screenshots
while win32api.GetAsyncKeyState(ord(QuitKey)) == 0:
    # Capture the screenshot using MSS
    screenshot = sct.grab(region)
    np_image = np.array(screenshot)

    # Convert RGB image to BGR (OpenCV uses BGR format)
    image_bgr = cv2.cvtColor(np_image, cv2.COLOR_RGB2BGR)

    # Resize the image to match the desired input shape
    image_resized = cv2.resize(image_bgr, (320, 240))

    # Display the screenshot
    # cv2.imshow('Debug',image_resized)

    # Normalize the image data /255
    image_norm = image_resized / 255.0

    # Expand dimensions to create a batch of size 1
    image_expanded = np.expand_dims(image_norm, axis=0)

    # Use the model to make predictions
    prediction = model.predict(image_expanded)

    # If any prediction is greater than 0.5, get the index of that prediction
    if np.any(prediction > 0.5):
        index = np.argmax(prediction)
        if index != 2:
            print(index)
            

        # Simulate key press based on the index
        key_stroke = key_mapping.get(index)
        # if key stroke is same as previous, dont release the key else press the new key
        if key_stroke != prev_key_stroke:
            if prev_key_stroke is not None:
                keyboard.release(prev_key_stroke)
            keyboard.press(key_stroke)
            prev_key_stroke = key_stroke


cv2.destroyAllWindows()
