from inference import InferencePipeline
from inference.core.interfaces.stream.sinks import render_boxes
import cv2
import os

class RoboflowFoodClassifier:
    def __init__(self, api_key="YOUR_ROBOFLOW_KEY"):
        self.pipeline = InferencePipeline.init(
            model_id="food-waste-classification-1/2",
            api_key=api_key,
            video_reference=0,  # Raspberry Pi camera
            on_prediction=self.handle_prediction
        )
        self.current_results = []

    def handle_prediction(self, prediction):
        self.current_results = prediction

    def classify_frame(self):
        self.pipeline.start()
        self.pipeline.join()
        return self.parse_results()

    def parse_results(self):
        waste_data = []
        for result in self.current_results:
            for box in result["predictions"]:
                waste_data.append({
                    "class": box["class"],
                    "confidence": box["confidence"],
                    "quantity_kg": self.estimate_quantity(box)
                })
        return waste_data

    def estimate_quantity(self, box):
        # Roboflow bbox dimensions to kg conversion (calibrate for your bins)
        area = (box["width"] * box["height"]) / 1000
        return round(area * 0.85, 2)  # 0.85kg per 1000px²
