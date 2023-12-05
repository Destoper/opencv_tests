import numpy as np
import cv2 as cv

# Load calibration data
calibration_data = np.load('calib_data/MultiMatrix.npz')

# Get camera matrix and distortion coefficients
mtx = calibration_data['camMatrix']
dist = calibration_data['distCoef']

# Read an image
img = cv.imread('images/image8.png')
h, w = img.shape[:2]

# Get optimal new camera matrix
newcameramtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))

# undistort
dst = cv.undistort(img, mtx, dist, None, newcameramtx)
# crop the image
x, y, w, h = roi
dst = dst[y:y+h, x:x+w]
cv.imwrite('calibresult.png', dst)