from ultralytics import YOLO
if __name__ == '__main__':
    # 加载模型
    model = YOLO(r'E:/AI_project/yoloV8/yolov8-main/ultralytics/models/v8/yolov8n.yaml')
    # 训练模型
    results = model.train(data=r'E:/AI_project/yoloV8/yolov8-main/ultralytics/datasets/coco8.yaml',  
                           cache=False,
                           imgsz=640,
                           epochs=100,
                           single_cls=False,  # 是否是单类别检测
                           batch=16,
                           close_mosaic=10,
                           workers=0,
                           device='0',
                           optimizer='SGD',
                           
                           project='runs/train',
                           name='exp',)