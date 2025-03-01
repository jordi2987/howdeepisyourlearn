import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.model_selection import TimeSeriesSplit
import joblib

def train():
    data = pd.read_csv("data/historical_waste.csv")
    data['hour'] = pd.to_datetime(data['timestamp']).dt.hour
    
    X = data[['hour', 'temperature', 'is_holiday']]
    y = data['weight_kg']
    
    model = Ridge(alpha=1.0)
    model.fit(X, y)
    
    joblib.dump(model, "regression_model.pkl")
