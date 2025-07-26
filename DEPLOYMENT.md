# 🚂 Déploiement sur Railway

## ✅ Votre application est prête pour Railway !

Tous les fichiers de configuration ont été créés et testés. Votre application de parfums peut maintenant être déployée sur Railway en quelques minutes.

## 🚀 Guide de déploiement

### 1. Prérequis
- ✅ Compte Railway (https://railway.app) - **GRATUIT**
- ✅ Code source sur GitHub/GitLab ou déploiement local
- ✅ Node.js (pour Railway CLI) - optionnel

### 2. Méthodes de déploiement

#### 🎯 **MÉTHODE RECOMMANDÉE: GitHub/GitLab**

1. **Poussez votre code sur GitHub/GitLab**
   ```bash
   git add .
   git commit -m "Prêt pour Railway"
   git push origin main
   ```

2. **Connectez à Railway**
   - Allez sur https://railway.app
   - Cliquez sur "New Project"
   - Sélectionnez "Deploy from GitHub repo"
   - Choisissez votre repository

3. **Configuration automatique**
   - ✅ Railway détecte automatiquement Flask
   - ✅ Utilise `Procfile` et `requirements.txt`
   - ✅ Configure Gunicorn automatiquement

#### 🛠️ **MÉTHODE ALTERNATIVE: Railway CLI**
1. **Installez Railway CLI**
   ```bash
   npm install -g @railway/cli
   ```

2. **Connectez-vous**
   ```bash
   railway login
   ```

3. **Initialisez le projet**
   ```bash
   railway init
   ```

4. **Déployez**
   ```bash
   railway up
   ```

### 3. Variables d'environnement

Configurez ces variables dans Railway Dashboard:

- `SECRET_KEY`: Clé secrète pour Flask (générez une clé sécurisée)
- `RAILWAY_ENVIRONMENT`: `production`
- `DATABASE_URL`: `sqlite:///velours_parfum.db` (ou PostgreSQL pour production)

### 4. Configuration de la base de données

#### SQLite (par défaut)
- Fonctionne pour les tests et petites applications
- Les données sont perdues à chaque redéploiement

#### PostgreSQL (recommandé pour production)
1. Ajoutez un service PostgreSQL dans Railway
2. Copiez l'URL de connexion
3. Mettez à jour `DATABASE_URL` avec l'URL PostgreSQL

### 5. Accès à l'application

Une fois déployée:
- **URL publique**: Railway vous fournira une URL (ex: https://your-app.railway.app)
- **Admin par défaut**:
  - Email: `admin@velours-parfum.com`
  - Mot de passe: `admin123`

### 6. Surveillance et logs

- **Logs**: Consultables dans Railway Dashboard
- **Métriques**: CPU, mémoire, requêtes
- **Redémarrages**: Automatiques en cas d'erreur

### 7. Domaine personnalisé (optionnel)

1. Dans Railway Dashboard, allez dans Settings
2. Ajoutez votre domaine personnalisé
3. Configurez les DNS selon les instructions

## 🔧 Fichiers de configuration

- `Procfile`: Commande de démarrage
- `requirements.txt`: Dépendances Python
- `gunicorn.conf.py`: Configuration du serveur
- `railway.json`: Configuration Railway
- `.env.example`: Variables d'environnement

## 🛠️ Dépannage

### Erreurs communes:
1. **Port binding**: Vérifiez que l'app écoute sur `0.0.0.0:$PORT`
2. **Dépendances**: Vérifiez `requirements.txt`
3. **Variables d'env**: Configurez toutes les variables nécessaires
4. **Base de données**: Vérifiez la connexion DB

### Logs utiles:
```bash
railway logs
```

## 📞 Support

- Documentation Railway: https://docs.railway.app
- Support Railway: https://railway.app/help
