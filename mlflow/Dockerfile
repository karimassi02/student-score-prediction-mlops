FROM python:3.13-slim

WORKDIR /app

RUN pip install --no-cache-dir mlflow pandas scikit-learn

COPY train_model.py .
COPY dataset.csv .

RUN python train_model.py

EXPOSE 8080

CMD ["mlflow", "server", "--host", "0.0.0.0", "--port", "8080", "--backend-store-uri", "sqlite:///mlflow.db", "--default-artifact-root", "./mlruns"]