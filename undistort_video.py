import cv2 as cv    
import numpy as np

def undistort_frame(frame, camMatrix, distCoeffs):
    h, w = frame.shape[:2]
    new_cam_matrix, roi = cv.getOptimalNewCameraMatrix(camMatrix, distCoeffs, (w, h), 1, (w, h))

    undistorted_frame = cv.undistort(frame, camMatrix, distCoeffs, None, new_cam_matrix)

    # Crop the image to remove black regions
    x, y, w, h = roi
    undistorted_frame = undistorted_frame[y:y+h, x:x+w]

    return undistorted_frame

def main():
    # Load calibration data
    data = np.load("calib_data/MultiMatrix.npz")
    camMatrix = data['camMatrix']
    distCoeffs = data['distCoef']

    # Open a connection to the camera
    cap = cv.VideoCapture(0)  # Adjust the index based on your camera setup

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Undistort the frame
        undistorted_frame = undistort_frame(frame, camMatrix, distCoeffs)

        # Display the original and undistorted frames
        cv.imshow('Original', frame)
        cv.imshow('Undistorted', undistorted_frame)

        # Press 'q' to exit the loop
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close all windows
    cap.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()
