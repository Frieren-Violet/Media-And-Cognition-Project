from pymycobot import MyCobot280
import time
import sys
import numpy as np
from robot_calib import M
mc = MyCobot280("COM11", 115200)
mc.power_on()
mc.release_all_servos()
"""
print("是否开始")
type = input("请输入")
if type == 'y':
    mc.power_on()
    coords = mc.get_coords()
    time.sleep(3)
    print(coords)
mc.power_off()
"""

xc = -20
yc = 10
pt = np.array([xc, yc, 1.0])
xr, yr = M @ pt
print(xr,yr)
mc.send_coords([xr, yr, 50, -156.13, -15.46, 142.41], 40, 0)


    