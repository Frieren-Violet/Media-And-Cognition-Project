import json
import time
import numpy as np
from pymycobot import MyCobot280


SERIAL_PORT = "COM11"
BAUD_RATE = 115200
PUMP_PIN = 5
mc= MyCobot280(SERIAL_PORT, BAUD_RATE)

zero=[172.7, 68.6, 299.6, -159.15, -0.41, -45.28]
BinA=[200.6, -150.3, 150.0, -159.15, -0.41, -45.28]  # TODO: 修改为实际投放点坐标
BinB=[150.0, 150.0, 150.0, -159.15, -0.41, -45.28]  # TODO: 修改为实际投放点坐标
BinC=[100.0, -150.0, 150.0, -159.15, -0.41, -45.28]  # TODO: 修改为实际投放点坐标
BinD=[200.0, 0.0, 150.0, -159.15, -0.41, -45.28]    # TODO: 修改为实际投放点坐标
Loading_Area=[250.0, 0.0, 150.0, -159.15, -0.41, -45.28]    # TODO: 修改为实际投放点坐标

def pump_on():
    mc.set_basic_output(5, 0)
    time.sleep(0.05)

def pump_off():
    # 关闭电磁阀
    mc.set_basic_output(5, 1)
    time.sleep(0.05)
    # 泄气阀门开始工作
    mc.set_basic_output(2, 0)
    time.sleep(1)
    mc.set_basic_output(2, 1)
    time.sleep(0.05)



def pixel_to_world(u, v):
    data = np.load("stereo_calib.npz")
    K_r = data["K_r"]; fx, fy = K_r[0,0], K_r[1,1]; cx, cy = K_r[0,2], K_r[1,2]
    Z = 350  # 物体据光心的距离，根据实际高度调整
    Xc = (u - cx) * Z / fx
    Yc = (v - cy) * Z / fy
    Pc = np.array([Xc, Yc, Z, 1.0])  # 相机坐标齐次

    T_cam2base = np.eye(4)  # TODO: 替换为标定得到的相机→机械臂基座外参
    Pw = T_cam2base @ Pc
    return Pw[0], Pw[1], Pw[2]

def load_best_target(path="yolo_results.json"):
    with open(path, "r", encoding="utf-8") as f:
        boxes = json.load(f)
    if not boxes:
        return None
    box = max(boxes, key=lambda b: b["conf"])
    x1, y1, x2, y2 = box["xyxy"]
    u, v = (x1 + x2) / 2, (y1 + y2) / 2
    return u, v, box

def pick():
    mc = MyCobot280(SERIAL_PORT, BAUD_RATE)
    mc.power_on()
    target = load_best_target()
    if not target:
        print("未找到目标")
        return
    u, v, info = target
    wx, wy, wz = pixel_to_world(u, v)
    pose_above = [wx, wy, wz + 35, -160, 0, -45]  # 末端姿态根据实际调整
    pose_pick  = [wx, wy, wz,     -160, 0, -45]

    mc.send_coords(zero, 100, 0)
    time.sleep(1.5)
    mc.send_coords(pose_above, 80, 0)
    time.sleep(1.0)
    mc.send_coords(pose_pick, 60, 0)
    time.sleep(0.8)
    pump_on(mc)
    mc.send_coords(pose_above, 80, 0)
    time.sleep(1.0)
    # TODO: 修改为你的投放点
    drop_pose = zero  
    mc.send_coords(drop_pose, 80, 0)
    time.sleep(1.0)
    pump_off(mc)

if __name__ == "__main__":
    pick()