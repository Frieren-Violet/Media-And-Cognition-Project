#用于拍摄相片
import cv2 as cv

def main():
    """
    name = "right"
    cap = cv.VideoCapture(0)
    flag = cap.isOpened() 
    while(cap.isOpened()):#检测是否在开启状态
        ret_flag,Vshow = cap.read()#得到每帧图像
        cv.imshow("Capture_Test",Vshow)#显示图像
        k = cv.waitKey(1) & 0xFF#按键判断
        if k == ord('s'):#保存
            cv.imwrite('E:/AI_project/git_set/Media-And-Cognition-Project/picture/test/' + name + ".jpg", Vshow)#保存路径
            print("success to save " + name + ".jpg")
            print("-------------------------")
        elif k == ord(' '):#空格退出
            break
    cap.release() 
    cv.destroyAllWindows()
    """
    name = "right"
    cap = cv.VideoCapture(0)
    ret_flag,Vshow = cap.read()#得到每帧图像
    cv.imwrite('E:/AI_project/git_set/Media-And-Cognition-Project/picture/test/right.jpg', Vshow)#保存路径
    print("success to save " + name + ".jpg")
    
if __name__ == '__main__':
    main()