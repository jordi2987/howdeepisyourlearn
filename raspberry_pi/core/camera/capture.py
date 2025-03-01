import cv2
import os
from datetime import datetime

def capture_image(save_dir="captures"):
    os.makedirs(save_dir, exist_ok=True)
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        raise IOError("Cannot access camera")
    
    ret, frame = cap.read()
    cap.release()
    
    if ret:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        img_path = f"{save_dir}/{timestamp}.jpg"
        cv2.imwrite(img_path, frame)
        return img_path
    else:
        raise RuntimeError("Image capture failed")
