#!/bin/bash

# Script de déploiement Streamlit sur Heroku

APP_NAME="karim-streamlit-app"

echo "🚀 Déploiement de Streamlit sur Heroku..."

# Login
heroku container:login

# Build
echo "📦 Build de l'image..."
docker build -t $APP_NAME .

# Tag
echo "🏷️  Tag de l'image..."
docker tag $APP_NAME registry.heroku.com/$APP_NAME/web

# Push
echo "⬆️  Push vers Heroku..."
docker push registry.heroku.com/$APP_NAME/web

# Release
echo "🎉 Release..."
heroku container:release web -a $APP_NAME

echo "✅ Déploiement terminé !"
echo "🌐 URL: https://$APP_NAME.herokuapp.com"