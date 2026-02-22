# Projet Final - Architecture IA Cloud

## Description
Application de prédiction ML avec architecture complète :
- **MLflow** : Gestion et hébergement des modèles
- **MCP Backend** : API de prédiction via FastMCP
- **Streamlit** : Interface utilisateur web

## Architecture

User → Streamlit (Heroku) → MCP Backend (Heroku) → MLflow (GCP/Codespace)

## Composants

### 1. MLflow
Serveur de tracking et hébergement de modèles ML.
- Dataset : Student Performance
- Modèle : Régression Linéaire (prédiction score)
- Déploiement : Google Cloud Run ou Codespace

### 2. MCP Backend
API FastMCP exposant des outils de prédiction.
- Liste les modèles disponibles
- Récupère le schéma d'entrée
- Effectue des prédictions
- Déploiement : Heroku

### 3. Streamlit Front
Interface web pour interagir avec le modèle.
- Formulaire de saisie
- Affichage des prédictions
- Déploiement : Heroku

## Déploiement

### MLflow sur GCP
```bash
cd mlflow
gcloud builds submit --tag gcr.io/[PROJECT_ID]/mlflow-server
gcloud run deploy mlflow-server --image gcr.io/[PROJECT_ID]/mlflow-server --platform managed



## MCP Backend sur Heroku

cd mcp-backend
heroku create karim-mcp-backend
heroku stack:set container -a karim-mcp-backend
docker build -t karim-mcp .
docker tag karim-mcp registry.heroku.com/karim-mcp-backend/web
docker push registry.heroku.com/karim-mcp-backend/web
heroku container:release web -a karim-mcp-backend


## Streamlit sur Heroku

cd streamlit-front
heroku create karim-streamlit-app
heroku stack:set container -a karim-streamlit-app
heroku config:set MCP_SERVER_URL=https://karim-mcp-backend.herokuapp.com/sse -a karim-streamlit-app
docker build -t karim-streamlit .
docker tag karim-streamlit registry.heroku.com/karim-streamlit-app/web
docker push registry.heroku.com/karim-streamlit-app/web
heroku container:release web -a karim-streamlit-app


Variables d'environnement

MCP Backend

MLFLOW_TRACKING_URI : URL du serveur MLflow
MLFLOW_MODEL_URI : URI du modèle (ex: models:/student_model/latest)


Streamlit

MCP_SERVER_URL : URL du serveur MCP
