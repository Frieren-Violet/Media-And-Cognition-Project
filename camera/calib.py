#双目相机标定
import cv2 as cv
import os

# 修改为你自己的摄像头编号
LEFT_CAM_ID  = 2
RIGHT_CAM_ID = 0

SAVE_DIR_LEFT  = "E:/AI_project/git_set/Media-And-Cognition-Project/picture/calibrate/left"
SAVE_DIR_RIGHT = "E:/AI_project/git_set/Media-And-Cognition-Project/picture/calibrate/right"

"""
os.makedirs(SAVE_DIR_LEFT, exist_ok=True)
os.makedirs(SAVE_DIR_RIGHT, exist_ok=True)

cap_l = cv.VideoCapture(LEFT_CAM_ID)
cap_r = cv.VideoCapture(RIGHT_CAM_ID)

# 固定分辨率（标定和使用必须一致）
WIDTH, HEIGHT = 640, 480
cap_l.set(cv.CAP_PROP_FRAME_WIDTH, WIDTH)
cap_l.set(cv.CAP_PROP_FRAME_HEIGHT, HEIGHT)
cap_r.set(cv.CAP_PROP_FRAME_WIDTH, WIDTH)
cap_r.set(cv.CAP_PROP_FRAME_HEIGHT, HEIGHT)

idx = 0
print("按 s 保存一组左右图，按 q 退出")

while True:
    ret_l, frame_l = cap_l.read()
    ret_r, frame_r = cap_r.read()

    if not ret_l or not ret_r:
        print("摄像头读取失败")
        break

    cv.imshow("Left", frame_l)
    cv.imshow("Right", frame_r)

    key = cv.waitKey(1) & 0xFF

    if key == ord('s'):
        idx += 1
        left_path  = f"{SAVE_DIR_LEFT}/{idx:02d}.jpg"
        right_path = f"{SAVE_DIR_RIGHT}/{idx:02d}.jpg"

        cv.imwrite(left_path, frame_l)
        cv.imwrite(right_path, frame_r)

        print(f"保存第 {idx} 组")

    elif key == ord('q'):
        break

cap_l.release()
cap_r.release()
cv.destroyAllWindows()

"""
import numpy as np
import glob

# ===== 棋盘参数 =====
BOARD_SIZE = (11, 8)      # 内角点数
SQUARE_SIZE = 20.0       # 每个格子的真实尺寸（mm）

# ===== 图片路径 =====
LEFT_PATH  = "E:/AI_project/git_set/Media-And-Cognition-Project/picture/calibrate/left/*.jpg"
RIGHT_PATH = "E:/AI_project/git_set/Media-And-Cognition-Project/picture/calibrate/right/*.jpg"

objp = np.zeros((BOARD_SIZE[0]*BOARD_SIZE[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:BOARD_SIZE[0], 0:BOARD_SIZE[1]].T.reshape(-1, 2)
objp *= SQUARE_SIZE

objpoints = []
imgpoints_l = []
imgpoints_r = []

left_images  = sorted(glob.glob(LEFT_PATH))
right_images = sorted(glob.glob(RIGHT_PATH))

assert len(left_images) == len(right_images), "左右图片数量不一致"

for l_img, r_img in zip(left_images, right_images):
    img_l = cv.imread(l_img)
    img_r = cv.imread(r_img)

    gray_l = cv.cvtColor(img_l, cv.COLOR_BGR2GRAY)
    gray_r = cv.cvtColor(img_r, cv.COLOR_BGR2GRAY)

    ret_l, corners_l = cv.findChessboardCorners(gray_l, BOARD_SIZE)
    ret_r, corners_r = cv.findChessboardCorners(gray_r, BOARD_SIZE)

    if ret_l and ret_r:
        objpoints.append(objp)

        corners_l = cv.cornerSubPix(
            gray_l, corners_l, (11,11), (-1,-1),
            (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
        )
        corners_r = cv.cornerSubPix(
            gray_r, corners_r, (11,11), (-1,-1),
            (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
        )

        imgpoints_l.append(corners_l)
        imgpoints_r.append(corners_r)


image_size = gray_l.shape[::-1]
print(image_size)
ret_l, K_l, dist_l, _, _ = cv.calibrateCamera(
    objpoints, imgpoints_l, image_size, None, None
)

ret_r, K_r, dist_r, _, _ = cv.calibrateCamera(
    objpoints, imgpoints_r, image_size, None, None
)

print("Left RMS:", ret_l)
print("Right RMS:", ret_r)


flags = cv.CALIB_FIX_INTRINSIC
#flags = cv.CALIB_USE_INTRINSIC_GUESS

ret, K_l, dist_l, K_r, dist_r, R, T, E, F = cv.stereoCalibrate(
    objpoints,
    imgpoints_l,
    imgpoints_r,
    K_l, dist_l,
    K_r, dist_r,
    image_size,
    criteria=(cv.TERM_CRITERIA_MAX_ITER + cv.TERM_CRITERIA_EPS, 100, 1e-5),
    flags=flags
)

print("Stereo RMS:", ret)
print("R:\n", R)
print("T:\n", T)

R1, R2, P1, P2, Q, roi1, roi2 = cv.stereoRectify(
    K_l, dist_l,
    K_r, dist_r,
    image_size,
    R, T,
    flags=cv.CALIB_ZERO_DISPARITY,
    alpha=1
)

print("Q matrix:\n", Q)

np.savez(
    "stereo_calib.npz",
    K_l=K_l,
    dist_l=dist_l,
    K_r=K_r,
    dist_r=dist_r,
    R=R,
    T=T,
    R1=R1,
    R2=R2,
    P1=P1,
    P2=P2,
    Q=Q,
    image_size=image_size
)

print("标定参数已保存到 stereo_calib.npz")







