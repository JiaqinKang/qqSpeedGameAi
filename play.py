import cv2
import numpy as np
import keras
import pyautogui
import pygetwindow as gw
from mss import mss

# Load model
model = keras.models.load_model('model2.h5')

# Find the QQ Speed window
window_name = 'QQ飞车2.0'  # Adjust this if the window name is different
qq_speed_window = gw.getWindowsWithTitle(window_name)[0]

# Mapping of index to key strokes
key_mapping = {
    0: 'left',
    1: 'right',
    2: 'up'
}

# Set up the MSS capture
region = {'top': qq_speed_window.top, 'left': qq_speed_window.left, 
          'width': qq_speed_window.width, 'height': qq_speed_window.height}
sct = mss()

# Main loop to capture and display screenshots
while True:
    # Capture the screenshot using MSS
    screenshot = sct.grab(region)
    np_image = np.array(screenshot)

    # Convert RGB image to BGR (OpenCV uses BGR format)
    image_bgr = cv2.cvtColor(np_image, cv2.COLOR_RGB2BGR)

    # Resize the image to match the desired input shape
    image_resized = cv2.resize(image_bgr, (320, 240))

    # Display the screenshot
    cv2.imshow('Debug',image_resized)

    # Normalize the image data /255
    image_norm = image_resized / 255.0

    # Expand dimensions to create a batch of size 1
    image_expanded = np.expand_dims(image_norm, axis=0)

    # Use the model to make predictions
    prediction = model.predict(image_expanded)

    # If any prediction is greater than 0.5, get the index of that prediction
    if np.any(prediction > 0.5):
        index = np.argmax(prediction)
        if index != 4:
            print(index)

        # Simulate key press based on the index
        key_stroke = key_mapping.get(index)
        if key_stroke:
            pyautogui.press(key_stroke)

    # Wait for a key press and check if 'q' was pressed to exit the loop
    if cv2.waitKey(1) == ord('q'):
        break

cv2.destroyAllWindows()
