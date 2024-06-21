import cv2 as cv
import numpy as np

# Create a Background Subtractor object with history and threshold settings
fgbg = cv.createBackgroundSubtractorMOG2(history=500, varThreshold=50)

def process(image):
    """
    Process the image to detect moving objects and draw bounding ellipses.

    Parameters:
    image (numpy.ndarray): The input image to process.

    Returns:
    numpy.ndarray: The processed image with detected objects highlighted.
    """
    # Apply the background subtractor to get the foreground mask
    mask = fgbg.apply(image)

    # Define a kernel for morphological operations
    kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (3, 3))

    # Apply morphological operations to clean up the mask
    mask = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel)
    mask = cv.morphologyEx(mask, cv.MORPH_CLOSE, kernel)
    mask = cv.dilate(mask, kernel, iterations=2)
    mask = cv.erode(mask, kernel, iterations=2)

    # Show the mask for debugging purposes
    cv.imshow("mask", mask)

    # Find contours in the mask
    contours, hierarchy = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    for c in range(len(contours)):
        # Calculate the area of each contour
        area = cv.contourArea(contours[c])
        if area < 500:  # Ignore small objects by area threshold
            continue
        # Get the minimum area rectangle that encloses the contour
        rect = cv.minAreaRect(contours[c])
        # Draw an ellipse around the detected object
        cv.ellipse(image, rect, (0, 255, 0), 2, 8)
        # Draw a circle at the center of the detected object
        cv.circle(image, (np.int32(rect[0][0]), np.int32(rect[0][1])), 2, (255, 0, 0), 2, 8, 0)
    return image

# Open the video file
vid_cap = cv.VideoCapture("people_walking.mp4")

while True:
    # Read each frame from the video
    ret, frame = vid_cap.read()
    if not ret:
        break
    # Process the frame
    result = process(frame)
    # Show the processed frame
    cv.imshow("result", result)
    # Exit the loop if the 'Esc' key is pressed
    k = cv.waitKey(50) & 0xff
    if k == 27:
        break

# Release the video capture object and close all OpenCV windows
vid_cap.release()
cv.destroyAllWindows()
