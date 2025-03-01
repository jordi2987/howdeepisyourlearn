import torch
import cv2
import numpy as np
from ultralytics import YOLO
from tensorflow.keras.models import load_model
import tensorflow.lite as tflite
import greengrasssdk
import sqlite3

# Load YOLOv8 model for object detection
yolo_model = YOLO('yolov8n.pt')

# Load U-Net segmentation model (assuming it's trained and converted to TFLite)
interpreter = tflite.Interpreter(model_path='unet_model.tflite')
interpreter.allocate_tensors()

# AWS Greengrass client
client = greengrasssdk.client('iot-data')

# Database setup
def initialize_db():
    conn = sqlite3.connect('food_waste.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS waste_data (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        food_item TEXT,
                        waste_amount REAL,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

def save_to_db(food_item, waste_amount):
    conn = sqlite3.connect('food_waste.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO waste_data (food_item, waste_amount) VALUES (?, ?)", (food_item, waste_amount))
    conn.commit()
    conn.close()

def preprocess_image(image):
    image = cv2.resize(image, (256, 256))
    image = image / 255.0
    image = np.expand_dims(image, axis=0)
    return image

def detect_food_waste(image_path):
    image = cv2.imread(image_path)
    results = yolo_model(image)
    
    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            crop_img = image[y1:y2, x1:x2]
            segment_and_report(crop_img)

def segment_and_report(crop_img):
    input_tensor_index = interpreter.get_input_details()[0]['index']
    output_tensor_index = interpreter.get_output_details()[0]['index']
    
    processed_img = preprocess_image(crop_img)
    interpreter.set_tensor(input_tensor_index, processed_img.astype(np.float32))
    interpreter.invoke()
    segmented_output = interpreter.get_tensor(output_tensor_index)
    
    waste_amount = np.sum(segmented_output)
    food_item = 'Detected'
    save_to_db(food_item, waste_amount)
    waste_data = {'food_item': food_item, 'waste_amount': waste_amount}
    report_to_cloud(waste_data)

def report_to_cloud(data):
    try:
        response = client.publish(
            topic='cafeteria/waste_report',
            payload=str(data)
        )
        print("Reported to AWS Greengrass:", data)
    except Exception as e:
        print("Failed to report:", e)

if __name__ == "__main__":
    initialize_db()
    detect_food_waste('waste_image.jpg')
