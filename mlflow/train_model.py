import pandas as pd
import mlflow
import mlflow.sklearn
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error, r2_score

# Chargement du dataset
data = pd.read_csv('dataset.csv')

# Préparation des features
X = data[['gender', 'parental_education', 'lunch_type', 'test_prep']]
y = data['score']

# Encodage des variables catégorielles
label_encoders = {}
for col in X.columns:
    le = LabelEncoder()
    X[col] = le.fit_transform(X[col])
    label_encoders[col] = le

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

# MLflow tracking
mlflow.set_experiment("student_score_prediction")

with mlflow.start_run():
    # Entraînement
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    # Prédictions
    y_pred = model.predict(X_test)
    
    # Métriques
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    # Logging
    mlflow.log_param("model_type", "LinearRegression")
    mlflow.log_param("test_size", 0.25)
    mlflow.log_metric("mse", mse)
    mlflow.log_metric("r2_score", r2)
    
    # Enregistrement du modèle
    mlflow.sklearn.log_model(
        model, 
        "model",
        registered_model_name="student_predictor"
    )
    
    print(f"Modèle entraîné - MSE: {mse:.2f}, R²: {r2:.2f}")