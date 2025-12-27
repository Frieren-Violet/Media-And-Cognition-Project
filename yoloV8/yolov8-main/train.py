from ultralytics import YOLO
if __name__ == '__main__':
    # 加载模型
    model = YOLO("yolov8n.pt")
    # 训练模型
    results = model.train(data="coco128.yaml",  
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