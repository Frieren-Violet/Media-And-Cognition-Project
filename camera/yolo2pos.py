#计算相机坐标系下的物块坐标
import numpy as np 
import json

# 导入参数(右相机内参)
data = np.load("stereo_calib.npz")
K_r = data["K_r"]
fx, fy = K_r[0,0], K_r[1,1]
cx, cy = K_r[0,2], K_r[1,2]

# 读取yolo物体框坐标
with open('yolo_results.json', 'r') as f:
    yolo_results = json.load(f)

best_obj = max(yolo_results, key=lambda x: x['conf'])

# 物体Z固定为35cm左右
Z = 350

x1, y1, x2, y2 = best_obj['xyxy']
u = (x1 + x2) / 2
v = (y1 + y2) / 2

# 像素 → 相机坐标
Xc = (u - cx) * Z / fx
Yc = (v - cy) * Z / fy
Zc = Z
Pc = np.array([Xc, Yc, Zc])
print(Pc)

np.savez(
    "cam_pos.npz",
    Pc = Pc 
)

print("物块相机坐标已保存到 cam_pos.npz")