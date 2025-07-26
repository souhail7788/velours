# Velours Parfum - E-commerce de Parfums de Luxe

Une application e-commerce complète pour la vente de parfums de luxe, développée avec Flask et Bootstrap.

## 🌟 Fonctionnalités

### Frontend (Boutique)
- **Catalogue de produits** avec recherche et filtres
- **Détails des produits** avec images et descriptions
- **Système de panier** avec gestion des quantités
- **Processus de commande** complet
- **Authentification utilisateur** (inscription/connexion)
- **Profil utilisateur** et historique des commandes
- **Design responsive** avec Bootstrap 5

### Backend (Administration)
- **Dashboard administrateur** avec statistiques
- **Gestion des produits** (CRUD complet)
- **Gestion des catégories**
- **Gestion des commandes** avec suivi des statuts
- **Upload d'images** pour les produits
- **Interface intuitive** et moderne

## 🚀 Installation et Configuration

### Prérequis
- Python 3.8+
- pip (gestionnaire de paquets Python)

### Installation

1. **Cloner le projet**
```bash
git clone <url-du-repo>
cd velours-parfum
```

2. **Créer un environnement virtuel** (recommandé)
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

4. **Initialiser la base de données**
```bash
python init_db.py
```

5. **Lancer l'application**
```bash
python app.py
```

L'application sera accessible sur `http://localhost:5000`

## 👤 Comptes par défaut

### Administrateur
- **Email :** admin@velours-parfum.com
- **Mot de passe :** admin123
- **Accès :** Dashboard admin complet

### Utilisateurs de test
- **jean.dupont@email.com** / password123
- **marie.martin@email.com** / password123
- **pierre.durand@email.com** / password123

## 📁 Structure du projet

```
velours-parfum/
├── app.py                 # Application Flask principale
├── models.py              # Modèles de base de données
├── routes.py              # Routes et contrôleurs
├── init_db.py            # Script d'initialisation
├── requirements.txt       # Dépendances Python
├── static/               # Fichiers statiques
│   ├── css/
│   │   └── style.css     # Styles personnalisés
│   ├── js/
│   │   └── main.js       # JavaScript personnalisé
│   └── images/
│       └── products/     # Images des produits
└── templates/            # Templates HTML
    ├── base.html         # Template de base
    ├── index.html        # Page d'accueil
    ├── products.html     # Catalogue
    ├── auth/             # Templates d'authentification
    └── admin/            # Templates d'administration
```

## 🛠️ Technologies utilisées

- **Backend :** Flask, SQLAlchemy, Flask-Login
- **Frontend :** Bootstrap 5, Font Awesome, JavaScript
- **Base de données :** SQLite (développement)
- **Upload d'images :** Pillow pour le redimensionnement
- **Sécurité :** Werkzeug pour le hachage des mots de passe

## 📊 Fonctionnalités détaillées

### Gestion des produits
- Ajout/modification/suppression de produits
- Upload et redimensionnement automatique des images
- Gestion des stocks
- Catégorisation des produits
- Activation/désactivation des produits

### Système de commandes
- Panier persistant en session
- Calcul automatique des totaux
- Gestion des frais de livraison
- Suivi des statuts de commande
- Historique complet des commandes

### Interface d'administration
- Dashboard avec statistiques en temps réel
- Gestion complète des produits et catégories
- Suivi des commandes avec changement de statut
- Interface responsive et intuitive

## 🎨 Personnalisation

### Couleurs et styles
Les couleurs principales sont définies dans `static/css/style.css` :
```css
:root {
    --primary-color: #8B4513;
    --secondary-color: #D2691E;
    --accent-color: #FFD700;
}
```

### Configuration
Les paramètres de l'application sont dans `app.py` :
- Clé secrète
- Configuration de la base de données
- Dossier d'upload des images

## 🔧 Développement

### Ajouter de nouvelles fonctionnalités
1. Modifier les modèles dans `models.py` si nécessaire
2. Ajouter les routes dans `routes.py`
3. Créer les templates HTML correspondants
4. Mettre à jour les styles CSS si besoin

### Base de données
Pour réinitialiser la base de données :
```bash
python init_db.py
```

## 📝 Notes importantes

- Les images sont automatiquement redimensionnées à 500x500px
- La livraison est gratuite pour les commandes > 50€
- Les mots de passe sont hachés avec Werkzeug
- L'application utilise SQLite par défaut (facile à changer)

## 🚀 Déploiement

Pour déployer en production :
1. Changer la clé secrète dans `app.py`
2. Configurer une base de données PostgreSQL/MySQL
3. Désactiver le mode debug
4. Configurer un serveur web (nginx + gunicorn)

## 📞 Support

Pour toute question ou problème, n'hésitez pas à consulter la documentation ou à créer une issue.

---

**Velours Parfum** - Votre destination pour les parfums de luxe 🌸
