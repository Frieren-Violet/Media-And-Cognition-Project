from pymycobot import MyCobot280
import time
import sys
import numpy as np
from robot_calib import M
SERIAL_PORT = "COM11"
BAUD_RATE = 115200
PUMP_PIN = 5  # 控制引脚
PUMP_DELAY = 0.5  # 吸泵操作延时
# 55.0, 150.32, -10.95, -86.9
loading_area = [244.4, 107.6, 87.4, 171.94, -15.5, -94.49]
"""
def pump_on(mc):#开启吸泵
    开启吸泵（低电平有效）
    mc.set_basic_output(PUMP_PIN, 0)
    time.sleep(PUMP_DELAY)
    print("吸泵已开启，开始吸附")

def pump_off(mc):#关闭吸泵
    关闭吸泵
    mc.set_basic_output(PUMP_PIN, 1)
    time.sleep(PUMP_DELAY)
    print("吸泵已关闭，已释放")
    mc.set_basic_output(2, 0)
    time.sleep(PUMP_DELAY)
    mc.set_basic_output(2, 1)
    time.sleep(PUMP_DELAY)
"""

data = np.load("cam_pos.npz")
Pc = data["Pc"]
print(Pc)

mc = MyCobot280(SERIAL_PORT, BAUD_RATE)

mc.power_on()
mc.release_all_servos()

pt = np.array([Pc[0], Pc[1], 1.0])
xr, yr = M @ pt
print(xr,yr)

mc.send_coords([xr, yr+25, 50.0, -155.32, -18.95, 160], 40, 0)
time.sleep(3)

