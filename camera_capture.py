import cv2 as cv
import os

# Tamanho do tabuleiro
CHESS_DIM = (14, 10)

image_counter = 0
image_dir_path = "images"

EXIST_IMAGE_DIR = os.path.isdir(image_dir_path)

if not EXIST_IMAGE_DIR:
    os.makedirs(image_dir_path)
    print(f"{image_dir_path} Directory is created")
else:
    print(f"{image_dir_path} Directory already exists")

criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

def detect_checker_board(image, grayImage, criteria, boardDimension):
    ret, corners = cv.findChessboardCorners(grayImage, boardDimension)
    if ret:
        corners_1 = cv.cornerSubPix(grayImage, corners, (3, 3), (-1, -1), criteria)
        image = cv.drawChessboardCorners(image, boardDimension, corners_1, ret)
    return image, ret

cap = cv.VideoCapture(0)

if not cap.isOpened():
    print("Error: Couldn't open the camera.")
    exit()

while True:
    _, frame = cap.read()
    copyFrame = frame.copy()
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    
    image, board_detected = detect_checker_board(frame, gray, criteria, CHESS_DIM)
    

    cv.putText(
        frame,
        f"saved_img: {image_counter}",
        (30, 40),
        cv.FONT_HERSHEY_PLAIN,
        1.4,
        (0, 255, 0),
        2,
        cv.LINE_AA
    )
    
    cv.imshow("frame", frame)
    cv.imshow("copyFrame", copyFrame)
    
    key = cv.waitKey(1)
    
    if key == ord("q"):
        break
    
    if key == ord("s") and board_detected:
        cv.imwrite(f"{image_dir_path}/image{image_counter}.png", copyFrame)
        print(f"saved image number {image_counter}")
        image_counter += 1

cap.release()
cv.destroyAllWindows()

print("Total saved Images", image_counter)
