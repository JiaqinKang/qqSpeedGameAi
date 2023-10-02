Auto-driving game AI with TensorFlow deep learning still needs to find a way to collect more data without accessing the game API.
- currently, the model is able to detect turns 

To extract more information is needed:
- [] Edges & Contours: Detect edges using techniques like the Canny edge detector. From these edges, contours (boundaries of objects) can be extracted.
- [] Hough Transforms: Detect specific shapes, like lines or circles, which can be useful for games with clear geometric elements.
- [] Color-based Segmentation: If certain game elements have distinct colors, segment the image based on color ranges in color spaces like HSV.
- Optical Character Recognition (OCR): Speed
If the game has readable text (like scores, timers, or stats) in the screenshot, use OCR techniques to extract this textual information.
- [] Semantic Segmentation
- Use deep learning models to classify each pixel in the screenshot, segmenting the image into meaningful regions (e.g., road, car, sky).
