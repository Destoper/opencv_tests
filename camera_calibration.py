import cv2 as cv    
import os
import numpy as np

CHESS_DIM = (9, 6)

#mm
VERTICE_SIZE = 18 

criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

calib_data_path = "calib_data"
EXIST_DIR = os.path.exists(calib_data_path)

if not EXIST_DIR:
    os.makedirs(calib_data_path)
    print(f"{calib_data_path} Directory is created")
else:
    print(f"{calib_data_path} Directory already exists")

# prepare object points
obj_3D = np.zeros((CHESS_DIM[0] * CHESS_DIM[1], 3), np.float32)
obj_3D[:,:2] = np.mgrid[0:CHESS_DIM[0], 0:CHESS_DIM[1]].T.reshape(-1, 2)
obj_3D *= VERTICE_SIZE
print(obj_3D)

# Array to store object points and image points from all the images.
obj_points_3D, img_points_2D = [], []

image_dir_path = "images"
files = os.listdir(image_dir_path)

for file in files:
    print(file)
    image_path = os.path.join(image_dir_path, file)

    image = cv.imread(image_path)
    grayScale = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    ret, corners = cv.findChessboardCorners(grayScale, CHESS_DIM, None)

    if ret:
        obj_points_3D.append(obj_3D)
        corners_2D = cv.cornerSubPix(grayScale, corners, (11, 11), (-1, -1), criteria)
        img_points_2D.append(corners_2D)

        img = cv.drawChessboardCorners(image, CHESS_DIM, corners_2D, ret)

        cv.imshow("Chessboard Corners", img)
        cv.waitKey(500) 

cv.destroyAllWindows()

# Calibrating
ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(obj_points_3D, img_points_2D, grayScale.shape[::-1], None, None)

print(" \nCALIBRATED")

print("duming the data into one files using numpy")
np.savez(
        f"{calib_data_path}/MultiMatrix", 
        camMatrix=mtx, 
        distCoef=dist, 
        rVector=rvecs, 
        tVector=tvecs)

print("="*50)
print("Loading data stored using numpy savez function \n \n \n")

data = np.load(f"{calib_data_path}/MultiMatrix.npz")

camMatrix = data['camMatrix']
distCoff = data['distCoef']
rVector = data['rVector']
tVector = data['tVector']

print("loaded calibration data sucefully")

# Re-projection Error
mean_error = 0
for i in range(len(obj_points_3D)):
    imgpoints2, _ = cv.projectPoints(obj_points_3D[i], rvecs[i], tvecs[i], mtx, dist)
    error = cv.norm(img_points_2D[i], imgpoints2, cv.NORM_L2)/len(imgpoints2)
    mean_error += error
print( "total error: {}".format(mean_error/len(obj_points_3D)) )