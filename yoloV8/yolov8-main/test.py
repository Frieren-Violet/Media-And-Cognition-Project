from ultralytics import YOLO
import json

def main(image_path, save_json=True):
    # 加载模型
    model = YOLO('yolov8m.pt')
    
    # 测试单张图片
    results = model.predict(source=image_path,
                            conf=0.25,
                            save=True,                              # 保存图片
                            show=True,                              # 显示图片
                            project='dataset/test/images_test',    # 保存目录
                            name='tp',
                            exist_ok=True   
                            )
    output_data = []

    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            conf = box.conf[0].item()
            cls = int(box.cls[0].item())
            output_data.append({
                'xyxy': [x1, y1, x2, y2],
                'conf': conf,
                'cls': cls
            })
    if save_json:
        with open('yolo_results.json', 'w') as f:
            json.dump(output_data, f)
    
    print("测试完成！结果保存在:yolo_results.json")
    return output_data

if __name__ == '__main__':
    main(image_path = 'E:/AI_project/picture/test/right.jpg')#测试图片路径