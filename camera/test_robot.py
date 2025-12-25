from pymycobot import MyCobot280
import time
import sys
import numpy as np

mc = MyCobot280("COM11", 115200)
mc.release_all_servos()
mc.power_on()
mc.send_coords([57.0, -107.4, 316.3, -93.81, -12.71, -160.49], 40, 1)
mc.power_off()