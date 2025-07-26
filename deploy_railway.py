#!/usr/bin/env python3
"""
Script de déploiement automatique sur Railway
"""

import os
import subprocess
import sys
import secrets

def check_requirements():
    """Vérifie que tous les fichiers nécessaires sont présents"""
    required_files = [
        'app.py',
        'wsgi.py', 
        'models.py',
        'routes.py',
        'requirements.txt',
        'Procfile',
        'gunicorn.conf.py'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Fichiers manquants: {', '.join(missing_files)}")
        return False
    
    print("✅ Tous les fichiers requis sont présents")
    return True

def generate_secret_key():
    """Génère une clé secrète sécurisée"""
    return secrets.token_hex(32)

def deploy_to_railway():
    """Déploie l'application sur Railway"""
    
    print("🚀 Déploiement sur Railway")
    print("=" * 50)
    
    # Vérifier les prérequis
    if not check_requirements():
        return False
    
    # Vérifier si Railway CLI est installé
    try:
        result = subprocess.run(['railway', '--version'], 
                              capture_output=True, text=True, check=True)
        print(f"✅ Railway CLI détecté: {result.stdout.strip()}")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Railway CLI n'est pas installé")
        print("💡 Installez-le avec: npm install -g @railway/cli")
        return False
    
    # Vérifier la connexion Railway
    try:
        subprocess.run(['railway', 'whoami'], 
                      capture_output=True, text=True, check=True)
        print("✅ Connecté à Railway")
    except subprocess.CalledProcessError:
        print("❌ Non connecté à Railway")
        print("💡 Connectez-vous avec: railway login")
        return False
    
    # Générer une clé secrète
    secret_key = generate_secret_key()
    print(f"🔑 Clé secrète générée: {secret_key[:16]}...")
    
    # Configurer les variables d'environnement
    env_vars = {
        'SECRET_KEY': secret_key,
        'RAILWAY_ENVIRONMENT': 'production',
        'DATABASE_URL': 'sqlite:///velours_parfum.db'
    }
    
    print("\n📋 Configuration des variables d'environnement...")
    for key, value in env_vars.items():
        try:
            cmd = ['railway', 'variables', 'set', f'{key}={value}']
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"   ✅ {key} configuré")
        except subprocess.CalledProcessError as e:
            print(f"   ❌ Erreur pour {key}: {e}")
            return False
    
    # Déployer l'application
    print("\n🚀 Déploiement en cours...")
    try:
        result = subprocess.run(['railway', 'up'], 
                              capture_output=True, text=True, check=True)
        print("✅ Déploiement réussi!")
        print(result.stdout)
        
        # Obtenir l'URL de l'application
        try:
            url_result = subprocess.run(['railway', 'domain'], 
                                      capture_output=True, text=True, check=True)
            url = url_result.stdout.strip()
            if url:
                print(f"\n🌐 Application disponible sur: {url}")
                print(f"👤 Admin: admin@velours-parfum.com / admin123")
            else:
                print("\n💡 Configurez un domaine avec: railway domain")
        except subprocess.CalledProcessError:
            print("\n💡 Configurez un domaine avec: railway domain")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur de déploiement: {e}")
        print(e.stderr)
        return False

def main():
    """Fonction principale"""
    print("🚂 Script de déploiement Railway")
    print("=" * 40)
    
    # Vérifier si nous sommes dans le bon répertoire
    if not os.path.exists('app.py'):
        print("❌ Veuillez exécuter ce script depuis le répertoire de l'application")
        return False
    
    # Demander confirmation
    response = input("\n❓ Voulez-vous déployer sur Railway? (y/N): ")
    if response.lower() not in ['y', 'yes', 'oui']:
        print("❌ Déploiement annulé")
        return False
    
    # Déployer
    success = deploy_to_railway()
    
    if success:
        print("\n🎉 Déploiement terminé avec succès!")
        print("\n📝 Prochaines étapes:")
        print("   1. Testez votre application")
        print("   2. Configurez un domaine personnalisé (optionnel)")
        print("   3. Surveillez les logs avec: railway logs")
    else:
        print("\n❌ Échec du déploiement")
        print("\n🔧 Dépannage:")
        print("   1. Vérifiez votre connexion Railway")
        print("   2. Consultez les logs: railway logs")
        print("   3. Vérifiez la documentation: https://docs.railway.app")
    
    return success

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
