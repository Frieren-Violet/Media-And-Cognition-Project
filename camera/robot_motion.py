from pymycobot import MyCobot280
import time
import sys
import numpy as np

data = np.load("cam_pos.npz")
Pc = data["Pc"]
print(Pc)
SERIAL_PORT = "COM11"
BAUD_RATE = 115200

mc = MyCobot280(SERIAL_PORT, BAUD_RATE)
time.sleep(1)

mc.release_all_servos()
time.sleep(1)
mc.power_on()
time.sleep(1)

rx =180
ry = 0
rz = 0

#mc.send_coords([Pc[0], Pc[1], Pc[2], rx, ry, rz], 40, 1)
mc.send_coords([57.0, -107.4, 316.3,rx, ry, rz], 40, 1)
time.sleep(1)
location = mc.get_coords()
print(location)

s = mc.is_controller_connected()
print(s)