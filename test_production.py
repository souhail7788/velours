#!/usr/bin/env python3
"""
Script pour tester l'application en mode production localement
"""

import os
import subprocess
import sys

def test_production():
    """Teste l'application avec la configuration de production"""
    
    print("🧪 Test de l'application en mode production...")
    
    # Définir les variables d'environnement pour simuler Railway
    env = os.environ.copy()
    env.update({
        'RAILWAY_ENVIRONMENT': 'production',
        'SECRET_KEY': 'test-secret-key-for-production',
        'PORT': '8080',
        'DATABASE_URL': 'sqlite:///parfume_store_prod_test.db'
    })
    
    print("📋 Variables d'environnement configurées:")
    for key, value in env.items():
        if key.startswith(('RAILWAY', 'SECRET', 'PORT', 'DATABASE')):
            print(f"   {key}={value}")
    
    print("\n🚀 Démarrage avec Gunicorn...")
    
    try:
        # Lancer l'application avec Gunicorn
        cmd = ['gunicorn', '--config', 'gunicorn.conf.py', 'app:app']
        process = subprocess.Popen(cmd, env=env)
        
        print(f"✅ Application démarrée avec PID {process.pid}")
        print("🌐 Accédez à: http://localhost:8080")
        print("👤 Admin: admin@parfume.com / admin123")
        print("\n⏹️  Appuyez sur Ctrl+C pour arrêter")
        
        # Attendre l'arrêt
        process.wait()
        
    except KeyboardInterrupt:
        print("\n🛑 Arrêt de l'application...")
        process.terminate()
        process.wait()
        print("✅ Application arrêtée")
        
    except FileNotFoundError:
        print("❌ Erreur: Gunicorn n'est pas installé")
        print("💡 Installez-le avec: pip install gunicorn")
        return False
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False
    
    return True

if __name__ == '__main__':
    success = test_production()
    sys.exit(0 if success else 1)
