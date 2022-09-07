"""
A FastAPI app to get predictions from a deployed model.
"""
import pandas as pd

from fastapi import FastAPI
from joblib import load
from pydantic import BaseModel


# Model for post request
class ModelParams(BaseModel):
    param1: str
    param2: str
    param3: int


app = FastAPI()

clf = load("/models/rf_best_estimator.pkl")


def get_prediction(param1, param2, param3):
    """
    Get predictions from a scikit-learn model.

    :param param1: GENDER
    :param param2: RACE
    :param param3: age_at_admittance
    """
    x = pd.DataFrame(
        {"GENDER": param1, "RACE": param2, "age_at_admittance": param3}, index=[0]
    )
    y = clf.predict(x)[0]
    prob = clf.predict_proba(x)[0].tolist()
    return {"prediction": int(y), "probability": prob}


@app.get("/")
async def read_root():
    return {"Model": "Random Forest Classifier"}


@app.get("/predict/{param1}/{param2}/{param3}")
async def predict(param1: str, param2: str, param3: int):
    pred = get_prediction(param1, param2, param3)
    return pred


@app.post("/predict-post/")
async def post_predict(params: ModelParams):
    pred = get_prediction(params.param1, params.param2, params.param3)
    return pred
