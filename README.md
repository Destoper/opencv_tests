# Camera Calibration and Undistortion Project

This project demonstrates camera calibration using OpenCV and provides a script to undistort images or live video feed using the calibrated camera parameters.

## Prerequisites

- Python 3
- OpenCV
- NumPy

## Getting Started

1. **Obtaining images for calibration:**
    - Set the correct `CHESS_DIM` (chessboard dimensions) on `camera_capture.py`.
    - Run `camera_capture.py`.
    - Press 'S' to save images.
    - Press 'Q' to stop.

1. **Calibrating :**
    - Set the correct `CHESS_DIM` on `camera_calibration.py`.
    - Set the correct `SIDE_SIZE` on `camera_calibration.py`.
    - Run `camera_calibration.py`.
    - The calibrated camera parameters will be saved in the `calib_data` folder.

### Part of the code was based on AiPhile Video Lessons: https://www.youtube.com/watch?v=JHeNger8B2E&t