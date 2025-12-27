import camera.shoot
import yoloV8.yolov8_main.test
import camera.yolo2pos
import camera.robot_motion

def run_program():
    # 拍摄图片
    camera.shoot.main()

    # 目标检测
    yoloV8.yolov8_main.test.main(
        image_path='E:/AI_project/git_set/Media-And-Cognition-Project/picture/test/right.jpg'
    )

    # 计算物块相机坐标
    camera.yolo2pos.main()

    # 机械臂运动
    camera.robot_motion.main()

if __name__ == '__main__':
    run_program()
