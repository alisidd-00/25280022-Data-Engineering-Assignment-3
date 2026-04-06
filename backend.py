from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
import numpy as np
from pathlib import Path

app = FastAPI(title="PakWheels Price Prediction API", version="1.0")

model_pipeline = None
MODEL_PATH = Path(__file__).resolve().parent / "pakwheels_svm_model.pkl"

class CarFeatures(BaseModel):
    year: float
    engine: float
    mileage: float
    transmission: str
    fuel: str
    body: str = "Sedan"
    city: str = "Lahore"

class PredictionResponse(BaseModel):
    prediction: int
    price_category: str
    confidence: str

@app.on_event("startup")
def load_model():
    global model_pipeline
    try:
        if not MODEL_PATH.exists():
            raise FileNotFoundError(
                f"Model file not found at: {MODEL_PATH}. "
                "Place pakwheels_svm_model.pkl in the project folder."
            )
        model_pipeline = joblib.load(MODEL_PATH)
        print(f"Model loaded successfully from: {MODEL_PATH}")
    except Exception as e:
        print(f"Error loading model: {e}")
        raise RuntimeError("Failed to load the trained model.")

@app.get("/")
def root():
    return {"message": "PakWheels Price Prediction API is running."}

@app.post("/predict", response_model=PredictionResponse)
def predict(car: CarFeatures):
    if model_pipeline is None:
        raise HTTPException(status_code=503, detail="Model not loaded")

    try:
        max_year_train = 2022.0
        car_age = max_year_train - car.year
        mileage_per_year = car.mileage / (car_age + 1)

        input_df = pd.DataFrame([{
            "year": car.year,
            "engine": car.engine,
            "mileage": car.mileage,
            "transmission": car.transmission,
            "fuel": car.fuel,
            "body": car.body,
            "city": car.city,
            "car_age": car_age,
            "mileage_per_year": mileage_per_year,
        }])

        prediction = int(model_pipeline.predict(input_df)[0])
        price_category = "High Price" if prediction == 1 else "Low Price"

        return PredictionResponse(
            prediction=prediction,
            price_category=price_category,
            confidence="Model prediction based on SVM classifier"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
