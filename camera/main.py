#代码借鉴
from pymycobot import MyCobot280
import time
import sys

SERIAL_PORT = "COM11"
BAUD_RATE = 115200
PUMP_PIN = 5  # 控制引脚
PUMP_DELAY = 1.0  # 吸泵操作延时

mc = MyCobot280(SERIAL_PORT, BAUD_RATE)
start=[158.0, 57.3, 116.2, 173.27, -9.62, 94.25]
end1=[252.4, 24.8, 222.2, 171.76, -69.27, -46.65]
end2=[172.8, 169.6, 251.8, -118.64, 2.3, 9.77]
end3=[135.5, 165.4, 226.8, 113.11, 36.98, -101.98]
end4=[149.1, -27.3, 236.4, -144.52, -42.36, -106.5]
zero=[172.7, 68.6, 299.6, -159.15, -0.41, -45.28]

def release_all(mc):
    mc.release_servo(1)
    mc.release_servo(2)
    mc.release_servo(3)
    mc.release_servo(4)
    mc.release_servo(5)
    mc.release_servo(6)
def get_pos(mc):
    mc.power_on()
    release_all(mc)
    print("🔧 位置调试模式")
    print("将机械臂手动移动到目标位置，然后按Enter键记录坐标")
    input("移动机械臂到目标位置，然后按Enter...")
    start = mc.get_coords()
    print(start)
    print("将机械臂手动移动到目标位置，然后按Enter键记录坐标")
    input("移动机械臂到目标位置，然后按Enter...")
    end=mc.get_coords()
    print(end)
    
    return start,end
#-------------------------吸泵---------------------------
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
#---------------------------------------------------------

def main(mc):
    mc.power_on()
    start_on=start.copy()
    start_on[2]+=50
    #移动到物体上方
    mc.send_coords(zero,100,0)
    time.sleep(3)
    #移动到物体处
    mc.send_coords(start,100,0)
    time.sleep(1.5)
    #吸取物体
    pump_on(mc)
    #回到高空zero处1
    mc.send_coords(zero,100,0)
    time.sleep(3)
    #移动到垃圾桶上方
    mc.send_coords(end4,80,0)
    time.sleep(2)
    #放下物体
    pump_off(mc)
    time.sleep(1)
    #mc.power_off()



if __name__ == "__main__":
    mc.power_on()
    print("选择模式:")
    print("1. 运行主程序")
    print("2. 调试/校准位置")
    choice = input("请输入选择 (1或2): ")
    
    if choice == "2":
        get_pos(mc)
    else:
        main(mc) 

    
mc.get_angles()
