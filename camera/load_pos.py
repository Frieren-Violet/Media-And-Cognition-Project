##备注：坏掉的应该是左侧相机
# 根据拍摄到的tag，计算参数，用来计算物体在tag坐标系中的坐标，似乎暂时没什么用
import json
import numpy as np
import cv2 as cv
from pupil_apriltags import Detector

data = np.load("stereo_calib.npz")
K_r = data["K_r"]
dist_r = data["dist_r"]

pic_path = 'E:/AI_project/picture/test/right.jpg'
img = cv.imread(pic_path)
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

gray = cv.equalizeHist(gray)

detector = Detector(families='tag16h5') 
tags = detector.detect(gray)
print(tags)
tag_size = 25.0 # mm

obj_pts = np.array([
    [-tag_size/2, -tag_size/2, 0],
    [ tag_size/2, -tag_size/2, 0],
    [ tag_size/2,  tag_size/2, 0],
    [-tag_size/2,  tag_size/2, 0]
], dtype=np.float32)

tag = tags[0]   # 假设只用一个 tag
img_pts = tag.corners.astype(np.float32)

ret, rvec, tvec = cv.solvePnP(
    obj_pts,
    img_pts,
    K_r,
    dist_r,
    flags=cv.SOLVEPNP_IPPE_SQUARE
)

R, _ = cv.Rodrigues(rvec)

fx, fy = K_r[0,0], K_r[1,1]
cx, cy = K_r[0,2], K_r[1,2]


"""
# 相机 → Tag 坐标系
P_tag = R.T @ (Pc - tvec)
print("object in tag frame (mm):", P_tag.ravel())
    
# 相机坐标 → 世界坐标
Pw = R @ Pc + tvec.flatten()
world_positions.append({'cls': obj['cls'], 'conf': obj['conf'], 'position': Pw.tolist()})
"""





