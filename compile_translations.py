#!/usr/bin/env python3
"""
Script pour compiler les fichiers de traduction .po en .mo
"""

import os
import subprocess
import sys

def compile_translations():
    """Compile tous les fichiers .po en .mo"""
    
    translations_dir = 'translations'
    
    if not os.path.exists(translations_dir):
        print(f"❌ Le dossier {translations_dir} n'existe pas")
        return False
    
    success = True
    
    # Parcourir tous les dossiers de langues
    for lang_dir in os.listdir(translations_dir):
        lang_path = os.path.join(translations_dir, lang_dir)
        
        if not os.path.isdir(lang_path):
            continue
            
        po_file = os.path.join(lang_path, 'LC_MESSAGES', 'messages.po')
        mo_file = os.path.join(lang_path, 'LC_MESSAGES', 'messages.mo')
        
        if os.path.exists(po_file):
            try:
                # Utiliser msgfmt pour compiler
                result = subprocess.run([
                    sys.executable, '-c',
                    f"""
import polib
po = polib.pofile('{po_file}')
po.save_as_mofile('{mo_file}')
print('✅ Compilé: {lang_dir}')
"""
                ], capture_output=True, text=True)
                
                if result.returncode == 0:
                    print(f"✅ Langue {lang_dir}: {po_file} -> {mo_file}")
                else:
                    print(f"❌ Erreur pour {lang_dir}: {result.stderr}")
                    success = False
                    
            except Exception as e:
                print(f"❌ Erreur pour {lang_dir}: {e}")
                success = False
        else:
            print(f"⚠️  Fichier .po manquant pour {lang_dir}")
    
    return success

if __name__ == '__main__':
    print("🌍 Compilation des traductions...")
    
    # Installer polib si nécessaire
    try:
        import polib
    except ImportError:
        print("📦 Installation de polib...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'polib'])
        import polib
    
    if compile_translations():
        print("✅ Toutes les traductions ont été compilées avec succès !")
    else:
        print("❌ Erreurs lors de la compilation")
        sys.exit(1)
