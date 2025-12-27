from pymycobot import MyCobot280
import time
import sys
import numpy as np
import os
import cv2 as cv

pred_points = np.array([
    [154.8054, -22.3679],
    [139.0244, -23.0103],
    [153.1764, -32.3247],
    [152.8420, -29.3787],
    [144.6224, -42.0850],
    [147.7516, -30.4268],
    [144.5203, -56.6333]
], dtype=np.float32)

# 真实坐标
real_points = np.array([
    [164.1, 8.8],
    [142.5, 3.2],
    [166.5, -15.7],
    [166.2, -9.4],
    [151.2, -40.7],
    [156.6, -17.6],
    [161.8, -32.6]
], dtype=np.float32)

# 估计仿射变换
X, inliers = cv.estimateAffine2D(pred_points, real_points)
print("预测坐标到实际坐标的补偿矩阵:\n", X)

given_points = np.array([
    [162.3273, -33.0948],
    [149.6468, -21.4619],
    [133.6215, -65.2749],
    [137.3588,  12.0139],
    [160.0421, -38.6392],
    [147.7184, -28.4409],
    [162.0801, -12.4182],
    [173.0624, -68.9065],
    [158.7390, -68.6802]
], dtype=np.float32)

# 实际坐标（机械臂真实到达）
reach_points = np.array([
    [151.5, -37.8],
    [146.8, -21.2],
    [131.7, -62.6],
    [135.7,   8.3],
    [158.6, -36.8],
    [139.2, -33.6],
    [158.6, -10.9],
    [174.2, -65.1],
    [158.8, -65.7]
], dtype=np.float32)

# 估计仿射变换
Y, inliers = cv.estimateAffine2D(given_points, reach_points)
Y_inv = cv.invertAffineTransform(Y)
print("运动坐标补偿矩阵:\n", Y_inv)

Bin_A = [161.8, 155.9, 150.0, -159.33, -16.4, -163.89]
Bin_D = [101.6, -186.0, 137.1, -149.26, -1.81, 69.82]
def main():
    base_dir = os.path.dirname(__file__)   # camera/
    calib_path = os.path.join(base_dir, "robot_calib.npz")
    M = np.load(calib_path)["M"]
    SERIAL_PORT = "COM11"
    BAUD_RATE = 115200
    PUMP_PIN = 5  # 控制引脚
    PUMP_DELAY = 0.5  # 吸泵操作延时
    # 55.0, 150.32, -10.95, -86.9
    loading_area = [244.4, 107.6, 87.4, 171.94, -15.5, -94.49]
    def pump_on(mc):#开启吸泵
        mc.set_basic_output(PUMP_PIN, 0)
        time.sleep(PUMP_DELAY)
        print("吸泵已开启，开始吸附")

    def pump_off(mc):#关闭吸泵
        mc.set_basic_output(PUMP_PIN, 1)
        time.sleep(PUMP_DELAY)
        print("吸泵已关闭，已释放")
   
    base_dir = os.path.dirname(__file__)   # camera/
    calib_path = os.path.join(base_dir, "cam_pos.npz")
    data = np.load(calib_path)
    Pc = data["Pc"]
    print(Pc)

    mc = MyCobot280(SERIAL_PORT, BAUD_RATE)

    mc.power_on()
    mc.release_all_servos()

    pump_off(mc)

    pt = np.array([Pc[0], Pc[1], 1.0])
    xr, yr = M @ pt
    print("预测坐标:", xr, yr)

    #预测坐标补偿
    vec = np.array([xr, yr, 1.0])
    x_c, y_c = X @ vec
    print("补偿预测坐标:", x_c, y_c)

    #运动坐标补偿
    vec = np.array([x_c, y_c, 1.0])
    x_e, y_e = Y_inv @ vec
    print("补偿运动坐标:", x_e, y_e)
    x_e += 15
    y_e += 10
    mc.send_coords([x_e, y_e, 60.0, -154.65, -19.53, 158.40], 80, 0)
    time.sleep(3)
    mc.send_coords([x_e, y_e, 30.0, -154.65, -19.53, 158.40], 80, 0)
    time.sleep(3)
    real = mc.get_coords()
    print("到达坐标:", real)   
    #吸取物体
    pump_on(mc)
    mc.send_coords([x_e, y_e, 180.0, -154.65, -19.53, 158.40], 80, 0)
    time.sleep(3)
    #移动到放置区上方
    mc.send_coords(Bin_D, 80, 0)
    time.sleep(3)
    #放置物体
    pump_off(mc)

    mc.power_off()

if __name__ == '__main__':
    main()