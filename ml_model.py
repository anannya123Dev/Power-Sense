import joblib
import numpy as np
import os
from sklearn.ensemble import RandomForestRegressor

MODEL_PATH = "model.pkl"

def train_and_save_model():
    np.random.seed(42)
    n = 500
    voltage  = np.random.uniform(210, 230, n)
    current  = np.random.uniform(0.5, 6.0, n)
    hybrid   = voltage * current * np.random.uniform(0.95, 1.05, n)
    total    = hybrid + np.random.uniform(-50, 50, n)

    X = np.column_stack([voltage, current, hybrid])
    y = total

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)
    joblib.dump(model, MODEL_PATH)
    print("Model trained and saved.")
    return model

# Cache the model in memory — load once, reuse every call
_model = None

def get_model():
    global _model
    if _model is None:
        if os.path.exists(MODEL_PATH):
            _model = joblib.load(MODEL_PATH)
        else:
            _model = train_and_save_model()
    return _model

def predict_power(voltage, current, hybrid_power):
    model = get_model()
    prediction = model.predict([[voltage, current, hybrid_power]])[0]
    return round(float(prediction), 2)

def classify_power(predicted_watts):
    if predicted_watts < 500:
        return "Low"
    elif predicted_watts < 1500:
        return "Medium"
    else:
        return "High"
