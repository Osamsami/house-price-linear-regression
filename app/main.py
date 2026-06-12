from fastapi import FastAPI, HTTPException
import joblib
import pandas as pd
import os

app = FastAPI(title="House Price Prediction API")

MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "model.pkl"
)

try:
    model = joblib.load(MODEL_PATH)
except Exception as error:
    model = None
    print(f"Model loading error: {error}")


MODEL_FEATURES = [
    "Id",
    "MSSubClass",
    "LotFrontage",
    "LotArea",
    "OverallQual",
    "OverallCond",
    "YearBuilt",
    "YearRemodAdd",
    "MasVnrArea",
    "BsmtFinSF1",
    "BsmtFinSF2",
    "BsmtUnfSF",
    "TotalBsmtSF",
    "1stFlrSF",
    "2ndFlrSF",
    "LowQualFinSF",
    "GrLivArea",
    "BsmtFullBath",
    "BsmtHalfBath",
    "FullBath",
    "HalfBath",
    "BedroomAbvGr",
    "KitchenAbvGr",
    "TotRmsAbvGrd",
    "Fireplaces",
    "GarageYrBlt",
    "GarageCars",
    "GarageArea",
    "WoodDeckSF",
    "OpenPorchSF",
    "EnclosedPorch",
    "3SsnPorch",
    "ScreenPorch",
    "PoolArea",
    "MiscVal",
    "MoSold",
    "YrSold"
]


@app.get("/")
def root():
    return {
        "message": "House Price Prediction API Running"
    }


@app.post("/predict")
def predict(features: dict):

    if model is None:
        raise HTTPException(
            status_code=500,
            detail="Model failed to load."
        )

    try:
        input_data = {
            feature: 0
            for feature in MODEL_FEATURES
        }

        input_data["Id"] = 1

        input_data.update(features)

        df = pd.DataFrame([input_data])

        df = df[MODEL_FEATURES]

        prediction = model.predict(df)

        return {
            "predicted_price": round(
                float(prediction[0]),
                2
            )
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )