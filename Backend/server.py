import sys
from pathlib import Path

# Add project root to Python path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from http.client import HTTPException
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from Core.prediction_helper import predict

class CreditRiskInput(BaseModel):
    age: int
    income: int
    loan_amount: int
    loan_tenure_months: int
    avg_dpd_per_delinquency: int
    delinquency_ratio_in_pc: int
    credit_utilization_ratio: int
    number_of_open_accounts: int
    residence_type: str
    loan_purpose: str
    loan_type: str

class CreditRiskOutput(BaseModel):
    probability: float
    credit_score: int
    rating: str

app=FastAPI()

@app.get("/test")
def test():
    return "Hello there!"

# Define a function predict_credit_risk
@app.post("/predict_credit_risk", response_model=CreditRiskOutput)

def predict_credit_risk(input_data: CreditRiskInput):
    try:
        input_dict = dict(input_data)
        probability, credit_score, rating = predict(input_dict)

        return CreditRiskOutput(probability=probability,credit_score=credit_score,rating=rating)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
