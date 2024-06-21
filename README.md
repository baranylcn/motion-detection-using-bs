# Motion Detection Using Background Subtraction

This project demonstrates a simple approach to detecting moving objects in a video using background subtraction and contour detection with OpenCV.

## Overview

The script processes a video file to detect moving objects by:

1. Applying background subtraction to generate a foreground mask.
2. Using morphological operations to clean the mask.
3. Finding contours in the cleaned mask.
4. Drawing ellipses and circles around detected objects based on their contours.
