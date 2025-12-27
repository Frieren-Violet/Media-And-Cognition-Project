import cv2
import numpy as np
import matplotlib.pyplot as plt

# 1. 读取生成的 16位 视差图 (必须加 -1 或 cv2.IMREAD_UNCHANGED)
# 请确保文件名和你生成的一致
img_path = 'Test_disparity.png' 
disp_16bit = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)

if disp_16bit is None:
    print("错误：找不到图片，请检查路径")
    exit()

# 2. 还原真实的视差数值 (float)
# 对应代码中的 img*256 操作，这里我们除回去
disp_true = disp_16bit.astype(np.float32) / 256.0

# 3. 打印中心点的视差值看看
h, w = disp_true.shape
center_disp = disp_true[h//2, w//2]
print(f"图像中心点的视差值是: {center_disp:.4f} 像素")

# 4. 生成彩色热力图 (为了好看)
# 归一化到 0-255 之间以便绘图
disp_vis = cv2.normalize(disp_true, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
# 应用伪彩色 (COLORMAP_JET 是常用的彩虹色，COLORMAP_MAGMA 是紫红色调)
disp_color = cv2.applyColorMap(disp_vis, cv2.COLORMAP_JET)

# 5. 显示和保存
# cv2.imshow("Disparity (Colorful)", disp_color)
cv2.imwrite("Test_disparity_color.png", disp_color) # 保存一份彩色的
print("已保存彩色可视化图片为 Test_disparity_color.png")

cv2.waitKey(0)
cv2.destroyAllWindows()