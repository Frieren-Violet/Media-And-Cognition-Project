from pymycobot import MyCobot280
import time
import sys
import numpy as np
from robot_calib import M
SERIAL_PORT = "COM11"
BAUD_RATE = 115200
PUMP_PIN = 5  # 控制引脚
PUMP_DELAY = 0.5  # 吸泵操作延时

loading_area = [224.4, 130.2, 86.1, -159.97, -10.64, -176.16]

def pump_on(mc):#开启吸泵
    """开启吸泵（低电平有效）"""
    mc.set_basic_output(PUMP_PIN, 0)
    time.sleep(PUMP_DELAY)
    print("吸泵已开启，开始吸附")

def pump_off(mc):#关闭吸泵
    """关闭吸泵"""
    mc.set_basic_output(PUMP_PIN, 1)
    time.sleep(PUMP_DELAY)
    print("吸泵已关闭，已释放")
    mc.set_basic_output(2, 0)
    time.sleep(PUMP_DELAY)
    mc.set_basic_output(2, 1)
    time.sleep(PUMP_DELAY)

data = np.load("cam_pos.npz")
Pc = data["Pc"]
print(Pc)

mc = MyCobot280(SERIAL_PORT, BAUD_RATE)

mc.power_on()
mc.release_all_servos()

pt = np.array([Pc[0], Pc[1], 1.0])
xr, yr = M @ pt

mc.send_coords([xr, yr, 35,-156.13, -15.46, 142.41], 40, 0)


s = mc.is_controller_connected()
print(s)