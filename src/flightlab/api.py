from datetime import date
from functools import lru_cache
from typing import Annotated

from fastapi import FastAPI, HTTPException, Query
from openai import OpenAIError
from pydantic import BaseModel, Field

from flightlab.analytics import summary
from flightlab.assistant import answer
from flightlab.data import load
from flightlab.model import load_model, predict

app = FastAPI(title="FlightLab", version="0.1.0", description="Analytics + ML + LLM de voos")


@lru_cache
def dataset():
    return load()[0]


@lru_cache
def model():
    return load_model()


class Flight(BaseModel):
    date: date
    carrier: str = Field(min_length=2, max_length=3, pattern=r"^[A-Z0-9]+$")
    origin: str = Field(pattern=r"^[A-Z]{3}$")
    dest: str = Field(pattern=r"^[A-Z]{3}$")
    distance: float = Field(gt=0, le=15000, allow_inf_nan=False)


class Question(BaseModel):
    question: str = Field(min_length=1, max_length=2000)
    use_llm: bool = False
    carrier: str | None = None


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/analytics")
def analytics(carrier: str | None = None, month: Annotated[int | None, Query(ge=1, le=12)] = None):
    try:
        df = dataset()
        if carrier:
            df = df.loc[df["carrier"].eq(carrier)]
        if month:
            df = df.loc[df["month"].eq(month)]
        return summary(df)
    except FileNotFoundError as error:
        raise HTTPException(503, str(error)) from error


@app.get("/model")
def model_metrics():
    try:
        return model()["metrics"]
    except FileNotFoundError as error:
        raise HTTPException(503, str(error)) from error


@app.post("/predict")
def prediction(flight: Flight):
    try:
        return predict(model(), flight.model_dump())
    except FileNotFoundError as error:
        raise HTTPException(503, str(error)) from error


@app.post("/assistant")
def assistant(question: Question):
    try:
        df = dataset()
        if question.carrier:
            df = df.loc[df["carrier"].eq(question.carrier)]
        return answer(question.question, df, question.use_llm)
    except FileNotFoundError as error:
        raise HTTPException(503, str(error)) from error
    except ValueError as error:
        raise HTTPException(422, str(error)) from error
    except OpenAIError as error:
        raise HTTPException(502, "O provedor de IA não respondeu. Tente novamente.") from error
