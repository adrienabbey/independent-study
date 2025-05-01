from ultralytics import YOLO

model = YOLO('yolov8s.yaml')  # or 'yolov8s.yaml' for better accuracy
model.train(data='./death-star-detector-3/data.yaml', epochs=20, imgsz=640)