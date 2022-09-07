FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

RUN pip install joblib pandas scikit-learn

COPY ./models /models
COPY ./app /app