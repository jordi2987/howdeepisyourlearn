import serial
import time
from camera.capture import capture_image
from ai.yolov8_inference import FoodWasteClassifier
from data.historical_waste import update_waste_log
from ordering.generate_orders import generate_order_list

arduino = serial.Serial('/dev/ttyACM0', 9600)
classifier = FoodWasteClassifier()

def main():
    while True:
        try:
            # 1. Capture Data
            img_path = capture_image()
            weight = float(arduino.readline().decode().strip())
            
            # 2. AI Analysis
            waste_data = classifier.classify(img_path)
            
            # 3. Update Records
            update_waste_log(waste_data, weight)
            
            # 4. Generate Orders
            order_list = generate_order_list()
            
            time.sleep(300)  # 5-minute intervals
            
        except Exception as e:
            print(f"Error: {str(e)}")
            time.sleep(10)

if __name__ == "__main__":
    main()
