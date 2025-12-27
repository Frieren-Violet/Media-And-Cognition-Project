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
    print("实际坐标:", coords)
mc.power_off()

#mc.send_coords([135.6, -53.8, 51.6, -156.93, -20.15, 145.45], 40, 1)
"""

from pymycobot import MyCobot320,PI_PORT
import time
arm=MyCobot320(PI_PORT,115200)
for i in range(2):
    arm.set_basic_output(1,0)#OUT1输出打开
    time.sleep(2)
    arm.set_basic_output(1,1)#OUT1输出关闭
    time.sleep(2)

"""
    