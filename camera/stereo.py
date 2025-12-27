#双目定位，暂时用不到
import numpy as np
import cv2 as cv
data = np.load("stereo_calib.npz")

K_l = data["K_l"]
dist_l = data["dist_l"]
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

def mouse_callback(event, x, y, flag, param):
    if event == cv.EVENT_LBUTTONDOWN:
        X, Y, Z = points_3d[y, x]
        print(f"pixel=({x},{y}) -> 3D=({X:.3f}, {Y:.3f}, {Z:.3f})")

left_path = 'E:/AI_project/git_set/Media-And-Cognition-Project/picture/test/left.jpg'
right_path = 'E:/AI_project/git_set/Media-And-Cognition-Project/picture/test/right.jpg'
left = cv.imread(left_path)
right = cv.imread(right_path)

map1x, map1y = cv.initUndistortRectifyMap(
    K_l, dist_l, R1, P1, image_size, cv.CV_32FC1
)
map2x, map2y = cv.initUndistortRectifyMap(
    K_r, dist_r, R2, P2, image_size, cv.CV_32FC1
)

left_rect = cv.remap(left, map1x, map1y, cv.INTER_LINEAR)
right_rect = cv.remap(right, map2x, map2y, cv.INTER_LINEAR)

stereo = cv.StereoSGBM_create(
    minDisparity=0,
    numDisparities=16*8,
    blockSize=5
)

disp = stereo.compute(left_rect, right_rect).astype(np.float32) / 16.0
points_3d = cv.reprojectImageTo3D(disp, Q)

cv.imshow("right", right)
cv.setMouseCallback("right", mouse_callback)
while True:
    cv.imshow("right", right)

    key = cv.waitKey(10) & 0xFF
    if key == 27:  # ESC 退出
        break

cv.destroyAllWindows()





