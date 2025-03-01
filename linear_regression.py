import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, KFold, cross_val_score
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
import sqlite3
import greengrasssdk

# AWS Greengrass client
client = greengrasssdk.client('iot-data')

# Database setup
def initialize_db():
    conn = sqlite3.connect('ordering_system.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS ingredient_orders (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        ingredient TEXT,
                        predicted_quantity REAL,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

def save_order(ingredient, predicted_quantity):
    conn = sqlite3.connect('ordering_system.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO ingredient_orders (ingredient, predicted_quantity) VALUES (?, ?)", (ingredient, predicted_quantity))
    conn.commit()
    conn.close()

def load_data():
    # Simulated dataset with seasonality, sales trends, and waste data
    data = pd.read_csv('ingredient_usage_data.csv')
    return data

def train_model(data):
    X = data[['seasonality', 'sales_trends', 'waste_data']]
    y = data['ingredient_usage']
    
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('regressor', LinearRegression())
    ])
    
    kf = KFold(n_splits=5, shuffle=True, random_state=42)
    scores = cross_val_score(pipeline, X, y, cv=kf, scoring='r2')
    
    pipeline.fit(X, y)
    print(f'Model trained with cross-validation R^2 scores: {scores.mean()}')
    return pipeline

def optimize_model(data):
    X = data[['seasonality', 'sales_trends', 'waste_data']]
    y = data['ingredient_usage']
    
    model = LinearRegression()
    param_grid = {'fit_intercept': [True, False], 'normalize': [True, False]}
    
    grid_search = GridSearchCV(model, param_grid, cv=5, scoring='r2')
    grid_search.fit(X, y)
    print(f'Best parameters: {grid_search.best_params_}')
    return grid_search.best_estimator_

def predict_orders(model, new_data):
    predictions = model.predict(new_data[['seasonality', 'sales_trends', 'waste_data']])
    for ingredient, predicted_quantity in zip(new_data['ingredient'], predictions):
        save_order(ingredient, predicted_quantity)
        report_to_cloud({'ingredient': ingredient, 'predicted_quantity': predicted_quantity})
    print("Orders predicted and saved.")

def report_to_cloud(data):
    try:
        response = client.publish(
            topic='cafeteria/order_predictions',
            payload=str(data)
        )
        print("Reported to AWS Greengrass:", data)
    except Exception as e:
        print("Failed to report:", e)

if __name__ == "__main__":
    initialize_db()
    data = load_data()
    model = train_model(data)
    optimized_model = optimize_model(data)
    new_data = pd.read_csv('new_ingredient_data.csv')  # New IoT data
    predict_orders(optimized_model, new_data)
