from pymycobot import MyCobot280
import time
import sys
import numpy as np
from robot_calib import M
mc = MyCobot280("COM11", 115200)
mc.power_on()
mc.release_all_servos()

print("是否开始")
type = input("请输入")
if type == 'y':
    mc.power_on()
    coords = mc.get_coords()
    time.sleep(3)
    print(coords)
mc.power_off()
"""

mc.send_coords([135.6, -53.8, 51.6, -156.93, -20.15, 145.45], 40, 1)
"""


    