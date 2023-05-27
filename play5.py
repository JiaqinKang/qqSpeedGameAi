import cv2
import numpy as np
import keras
import pygetwindow as gw
from mss import mss
import time
import win32api
import pyautogui

# Load model
model = keras.models.load_model('model9.h5')
prev_key_stroke = None
QuitKey = 'Q'

# Find the QQ Speed window
window_name = 'QQ飞车2.0'  # Adjust this if the window name is different
qq_speed_window = gw.getWindowsWithTitle(window_name)[0]

# Mapping of index to key strokes
key_mapping = {
    0: 'left',
    1: 'right',
}

# Set up the MSS capture
region = {'top': qq_speed_window.top, 'left': qq_speed_window.left,
          'width': qq_speed_window.width, 'height': qq_speed_window.height}
sct = mss()

# Main loop to capture and display screenshots
while win32api.GetAsyncKeyState(ord(QuitKey)) == 0:

    # Capture the screenshot using MSS
    screenshot = sct.grab(region)
    np_image = np.array(screenshot)

    # Convert RGB image to BGR (OpenCV uses BGR format)
    image_bgr = cv2.cvtColor(np_image, cv2.COLOR_RGB2BGR)

    # Resize the image to match the desired input shape
    image_resized = cv2.resize(image_bgr, (320, 240))

    # Normalize the image data /255
    image_norm = image_resized / 255.0

    # Expand dimensions to create a batch of size 1
    image_expanded = np.expand_dims(image_norm, axis=0)

    # Use the model to make predictions
    prediction = model.predict(image_expanded)

    # get max index of prediction
    index = np.argmax(prediction)
    print(index)

    # Press the key corresponding to the prediction
    if index in key_mapping:
        key_stroke = key_mapping.get(index)
        # if key stroke is same as previous, dont release the key else press the new key
        if key_stroke != prev_key_stroke:
            if prev_key_stroke is not None:
                pyautogui.keyUp(prev_key_stroke)
            prev_key_stroke = key_stroke
            pyautogui.keyDown(key_stroke)
        else:
            prev_key_stroke = key_stroke

    # Wait for a key press and check if 'q' was pressed to exit the loop
    if cv2.waitKey(1) == ord('q'):
        break

# Release the key
if prev_key_stroke is not None:
    pyautogui.keyUp(prev_key_stroke)

cv2.destroyAllWindows()
