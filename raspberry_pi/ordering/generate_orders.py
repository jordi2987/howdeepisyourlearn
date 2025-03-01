import joblib
import pandas as pd
from datetime import datetime

def generate_order_list():
    model = joblib.load("regression_model.pkl")
    current_hour = datetime.now().hour
    weather_data = get_live_weather()  # Implement API call
    
    prediction = model.predict([[current_hour, weather_data['temp'], 0]])
    return {"chicken": prediction[0], "rice": prediction[0]*0.7}
