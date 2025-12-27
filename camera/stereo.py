#双目定位，暂时用不到
import numpy as np
import cv2 as cv
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
calib_path = os.path.join(BASE_DIR, "stereo_calib.npz")

data = np.load(calib_path)

K_l = data["K_l"]
dist_l= data["dist_l"]
K_r = data["K_r"]
dist_r = data["dist_r"]
R = data["R"]
T = data["T"]
R1 = data["R1"]
R2 = data["R2"]
P1 = data["P1"]
P2 = data["P2"]
Q = data["Q"]
image_size = tuple(data["image_size"])
print("Loaded stereo calibration parameters.", Q)

def mouse_callback(event, x, y, flag, param):
    if event == cv.EVENT_LBUTTONDOWN:
        X, Y, Z = points_3d[y, x]
        print(f"pixel=({x},{y}) -> 3D=({X:.3f}, {Y:.3f}, {Z:.3f})")

left_path = 'E:/AI_project/git_set/Media-And-Cognition-Project/picture/test/left/01.jpg'
right_path = 'E:/AI_project/git_set/Media-And-Cognition-Project/picture/test/right/01.jpg'
left = cv.imread(left_path)
right = cv.imread(right_path)

map1x, map1y = cv.initUndistortRectifyMap(
    K_l, dist_l, R1, P1, image_size, cv.CV_32FC1
)
map2x, map2y = cv.initUndistortRectifyMap(
    K_r, dist_r, R2, P2, image_size, cv.CV_32FC1
)

left_rect = cv.remap(left, map1x, map1y, cv.INTER_CUBIC)
right_rect = cv.remap(right, map2x, map2y, cv.INTER_CUBIC)

cv.imshow("pic", right)

# SGBM 参数
stereo = cv.StereoSGBM_create(
    minDisparity=0,
    numDisparities=192,
    blockSize=7,
    P1=8*3*7**2,
    P2=32*3*7**2,
    disp12MaxDiff=1,
    uniquenessRatio=10,
    speckleWindowSize=50,
    speckleRange=2
)

disp = stereo.compute(left_rect, right_rect).astype(np.float32) / 16.0
disp_vis = cv.normalize(disp, None, 0, 255, cv.NORM_MINMAX).astype(np.uint8)
cv.imshow("disp", disp_vis)
cv.waitKey(100)

# 将无效视差点设为0或NaN
disp[disp <= 0] = np.nan
points_3d = cv.reprojectImageTo3D(disp, Q)

cv.imshow("left", left_rect)
cv.setMouseCallback("left", mouse_callback)
while True:
    cv.imshow("left", left_rect)

    key = cv.waitKey(10) & 0xFF
    if key == 27:  # ESC 退出
        break

cv.destroyAllWindows()





