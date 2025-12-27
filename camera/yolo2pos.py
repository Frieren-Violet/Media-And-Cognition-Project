#计算相机坐标系下的物块坐标
import numpy as np 
import json
import cv2 as cv
import os

def main():
    # 导入参数(右相机内参)
    current_dir = os.path.dirname(__file__)
    calib_path = os.path.join(current_dir, "calib_right.npz")
    data = np.load(calib_path)
    K = data["K"]
    dist = data["dist"]
    fx, fy = K[0,0], K[1,1]
    cx, cy = K[0,2], K[1,2]

    # 读取yolo物体框坐标
    current_dir = os.path.dirname(__file__)
    json_path = os.path.join(current_dir, "yolo_results.json")
    with open(json_path, 'r') as f:
        yolo_results = json.load(f)

    best_obj = max(yolo_results, key=lambda x: x['conf'])

    # 物体Z固定为35cm左右
    Z = 350

    x1, y1, x2, y2 = best_obj['xyxy']
    u = (x1 + x2) / 2
    v = (y1 + y2) / 2
    print(u, v)
    # 像素 → 相机坐标
    # 构造像素点 (N,1,2)
    pts = np.array([[[u, v]]], dtype=np.float32)

    # 去畸变 + 归一化
    undistorted = cv.undistortPoints(pts, K, dist)

    # 这是归一化相机坐标 (x', y')
    x_norm, y_norm = undistorted[0, 0]
    Xc = x_norm * Z 
    Yc = y_norm * Z
    Zc = Z
    Pc = np.array([Xc, Yc, Zc])
    print(Pc)
    np.savez(
        "./camera/cam_pos.npz",
        Pc = Pc 
    )

    print("物块相机坐标已保存到 cam_pos.npz")

if __name__ == '__main__':
    main()

'''
Z = 350
right_path = 'E:/AI_project/git_set/Media-And-Cognition-Project/picture/test/right.jpg'
right = cv.imread(right_path)
def mouse_callback(event, x, y, flag, param): 
    if event == cv.EVENT_LBUTTONDOWN: 
        Xc = (x - cx) * Z / fx
        Yc = (y - cy) * Z / fy 
        print(f"pixel=({x},{y}) -> 2D=({Xc:.3f}, {Yc:.3f})")

cv.imshow("right", right) 
cv.setMouseCallback("right", mouse_callback) 
while True: 
    cv.imshow("right", right) 
    key = cv.waitKey(10) & 0xFF 
    if key == 27: # ESC 退出 
        break 

cv.destroyAllWindows()
'''