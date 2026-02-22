import os
from typing import Any, Dict, List, Optional, Union
import mlflow
import pandas as pd
from fastmcp import FastMCP
import requests

mcp = FastMCP("StudentScorePredictor")


def setup_mlflow():
    """Configure MLflow tracking URI"""
    tracking_uri = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:8080")
    mlflow.set_tracking_uri(tracking_uri)
    print(f"[MLflow] Connected to: {tracking_uri}")


def get_model_uri():
    """Récupère l'URI du modèle depuis les variables d'env"""
    model_uri = os.getenv("MLFLOW_MODEL_URI", "models:/student_predictor/latest")
    return model_uri


# Cache pour éviter de recharger le modèle à chaque appel
_model_cache = {}


def load_model(model_uri: str):
    """Charge le modèle MLflow avec cache"""
    setup_mlflow()
    
    if model_uri not in _model_cache:
        print(f"[Model] Loading from: {model_uri}")
        _model_cache[model_uri] = mlflow.pyfunc.load_model(model_uri)
    
    return _model_cache[model_uri]


@mcp.tool()
def list_models() -> Dict[str, Any]:
    """Liste les modèles enregistrés dans MLflow"""
    try:
        setup_mlflow()
        tracking_uri = os.getenv("MLFLOW_TRACKING_URI")
        
        response = requests.get(
            f"{tracking_uri}/api/2.0/mlflow/registered-models/search"
        )
        response.raise_for_status()
        
        data = response.json()
        models = [m["name"] for m in data.get("registered_models", [])]
        
        return {"models": models, "count": len(models)}
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def get_input_schema(model_uri: Optional[str] = None) -> Dict[str, Any]:
    """Retourne le schéma d'entrée attendu par le modèle"""
    try:
        uri = model_uri or get_model_uri()
        model = load_model(uri)
        
        signature = getattr(getattr(model, "metadata", None), "signature", None)
        
        if signature is None or signature.inputs is None:
            # Schéma par défaut pour notre modèle
            return {
                "model_uri": uri,
                "inputs": [
                    {"name": "gender", "type": "string", "values": ["male", "female"]},
                    {"name": "parental_education", "type": "string", "values": ["high school", "some college", "associate", "bachelor", "master"]},
                    {"name": "lunch_type", "type": "string", "values": ["standard", "free/reduced"]},
                    {"name": "test_prep", "type": "string", "values": ["none", "completed"]}
                ]
            }
        
        inputs = []
        for col in signature.inputs.inputs:
            inputs.append({"name": col.name, "type": str(col.type)})
        
        return {"model_uri": uri, "inputs": inputs}
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def predict_score(
    gender: str,
    parental_education: str,
    lunch_type: str,
    test_prep: str,
    model_uri: Optional[str] = None
) -> Dict[str, Any]:
    """
    Prédit le score d'un étudiant
    
    Args:
        gender: "male" ou "female"
        parental_education: niveau d'éducation des parents
        lunch_type: "standard" ou "free/reduced"
        test_prep: "none" ou "completed"
    """
    try:
        uri = model_uri or get_model_uri()
        model = load_model(uri)
        
        # Création du DataFrame d'entrée
        input_data = pd.DataFrame([{
            "gender": gender,
            "parental_education": parental_education,
            "lunch_type": lunch_type,
            "test_prep": test_prep
        }])
        
        # Prédiction
        prediction = model.predict(input_data)
        score = float(prediction[0])
        
        return {
            "predicted_score": round(score, 2),
            "input": {
                "gender": gender,
                "parental_education": parental_education,
                "lunch_type": lunch_type,
                "test_prep": test_prep
            },
            "model_uri": uri
        }
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def batch_predict(
    students: List[Dict[str, str]],
    model_uri: Optional[str] = None
) -> Dict[str, Any]:
    """
    Prédit les scores pour plusieurs étudiants
    
    Args:
        students: Liste de dictionnaires avec les données de chaque étudiant
    """
    try:
        uri = model_uri or get_model_uri()
        model = load_model(uri)
        
        # Création du DataFrame
        input_data = pd.DataFrame(students)
        
        # Prédictions
        predictions = model.predict(input_data)
        
        results = []
        for i, pred in enumerate(predictions):
            results.append({
                "student_index": i,
                "predicted_score": round(float(pred), 2),
                "input": students[i]
            })
        
        return {
            "predictions": results,
            "count": len(results),
            "model_uri": uri
        }
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    print(f"🚀 MCP Server starting on port {port}")
    mcp.run("sse", host="0.0.0.0", port=port)