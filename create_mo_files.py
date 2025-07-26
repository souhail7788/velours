#!/usr/bin/env python3
"""
Script pour créer les fichiers .mo à partir des traductions
"""

import os
import struct

def create_mo_file(translations, output_path):
    """Crée un fichier .mo à partir d'un dictionnaire de traductions"""

    # Créer le dossier si nécessaire
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Ajouter l'entrée vide pour les métadonnées
    translations_with_meta = {"": "Content-Type: text/plain; charset=UTF-8\n"}
    translations_with_meta.update(translations)

    # Préparer les données
    keys = list(translations_with_meta.keys())
    values = list(translations_with_meta.values())

    # Encoder en UTF-8
    kencoded = [k.encode('utf-8') for k in keys]
    vencoded = [v.encode('utf-8') for v in values]

    # Calculer les offsets
    keystart = 7 * 4 + 16 * len(keys)
    valuestart = keystart + sum(len(k) for k in kencoded)

    # Créer les index
    koffsets = []
    voffsets = []

    # Offsets des clés
    offset = keystart
    for k in kencoded:
        koffsets.append((len(k), offset))
        offset += len(k)

    # Offsets des valeurs
    offset = valuestart
    for v in vencoded:
        voffsets.append((len(v), offset))
        offset += len(v)

    # Écrire le fichier
    with open(output_path, 'wb') as f:
        # Magic number (little endian)
        f.write(struct.pack('<I', 0x950412de))
        # Version
        f.write(struct.pack('<I', 0))
        # Nombre d'entrées
        f.write(struct.pack('<I', len(keys)))
        # Offset des clés
        f.write(struct.pack('<I', 7 * 4))
        # Offset des valeurs
        f.write(struct.pack('<I', 7 * 4 + 8 * len(keys)))
        # Hash table size (0)
        f.write(struct.pack('<I', 0))
        # Hash table offset (0)
        f.write(struct.pack('<I', 0))

        # Index des clés
        for length, offset in koffsets:
            f.write(struct.pack('<I', length))
            f.write(struct.pack('<I', offset))

        # Index des valeurs
        for length, offset in voffsets:
            f.write(struct.pack('<I', length))
            f.write(struct.pack('<I', offset))

        # Données des clés
        for k in kencoded:
            f.write(k)

        # Données des valeurs
        for v in vencoded:
            f.write(v)

# Traductions anglaises
english_translations = {
    "Accueil": "Home",
    "Produits": "Products", 
    "Panier": "Cart",
    "Admin": "Admin",
    "Connexion": "Login",
    "Inscription": "Register",
    "Déconnexion": "Logout",
    "Mon Profil": "My Profile",
    "Mes Commandes": "My Orders",
    "Bienvenue chez Velours Parfum": "Welcome to Velours Parfum",
    "Découvrez notre collection exclusive de parfums de luxe et laissez-vous envoûter par des fragrances veloutées d'exception": "Discover our exclusive collection of luxury perfumes and let yourself be enchanted by exceptional velvety fragrances",
    "Découvrir nos produits": "Discover our products",
    "Explorer": "Explore",
    "Produits en vedette": "Featured Products",
    "Nos Catégories": "Our Categories",
    "Description": "Description",
    "Aucune description disponible.": "No description available.",
    "Ajouter au panier": "Add to cart",
    "Quantité": "Quantity",
    "En stock": "In stock",
    "Rupture de stock": "Out of stock",
    "Informations produit": "Product information",
    "Volume": "Volume",
    "Genre": "Gender",
    "Mon Panier": "My Cart",
    "Votre panier est vide": "Your cart is empty",
    "Découvrez notre sélection de parfums et ajoutez vos favoris !": "Discover our selection of perfumes and add your favorites!",
    "Total": "Total",
    "Finaliser la commande": "Checkout",
    "Continuer les achats": "Continue shopping",
    "Email": "Email",
    "Mot de passe": "Password",
    "Se connecter": "Sign in",
    "Pas encore de compte ?": "Don't have an account?",
    "Créer un compte": "Create account",
    "Nom d'utilisateur": "Username",
    "S'inscrire": "Sign up",
    "Déjà un compte ?": "Already have an account?",
    "Votre destination pour les parfums de luxe": "Your destination for luxury perfumes",
    "Tous droits réservés.": "All rights reserved."
}

# Traductions espagnoles
spanish_translations = {
    "Accueil": "Inicio",
    "Produits": "Productos",
    "Panier": "Carrito", 
    "Admin": "Admin",
    "Connexion": "Iniciar sesión",
    "Inscription": "Registrarse",
    "Déconnexion": "Cerrar sesión",
    "Mon Profil": "Mi Perfil",
    "Mes Commandes": "Mis Pedidos",
    "Bienvenue chez Velours Parfum": "Bienvenido a Velours Parfum",
    "Découvrez notre collection exclusive de parfums de luxe et laissez-vous envoûter par des fragrances veloutées d'exception": "Descubre nuestra colección exclusiva de perfumes de lujo y déjate encantar por fragancias aterciopeladas excepcionales",
    "Découvrir nos produits": "Descubrir nuestros productos",
    "Explorer": "Explorar",
    "Produits en vedette": "Productos destacados",
    "Nos Catégories": "Nuestras Categorías",
    "Description": "Descripción",
    "Aucune description disponible.": "No hay descripción disponible.",
    "Ajouter au panier": "Añadir al carrito",
    "Quantité": "Cantidad",
    "En stock": "En stock",
    "Rupture de stock": "Agotado",
    "Informations produit": "Información del producto",
    "Volume": "Volumen",
    "Genre": "Género",
    "Mon Panier": "Mi Carrito",
    "Votre panier est vide": "Tu carrito está vacío",
    "Découvrez notre sélection de parfums et ajoutez vos favoris !": "¡Descubre nuestra selección de perfumes y añade tus favoritos!",
    "Total": "Total",
    "Finaliser la commande": "Finalizar pedido",
    "Continuer les achats": "Continuar comprando",
    "Email": "Email",
    "Mot de passe": "Contraseña",
    "Se connecter": "Iniciar sesión",
    "Pas encore de compte ?": "¿No tienes cuenta?",
    "Créer un compte": "Crear cuenta",
    "Nom d'utilisateur": "Nombre de usuario",
    "S'inscrire": "Registrarse",
    "Déjà un compte ?": "¿Ya tienes cuenta?",
    "Votre destination pour les parfums de luxe": "Tu destino para perfumes de lujo",
    "Tous droits réservés.": "Todos los derechos reservados."
}

# Traductions françaises (identiques)
french_translations = {k: k for k in english_translations.keys()}

if __name__ == '__main__':
    print("🌍 Création des fichiers .mo...")
    
    # Créer les fichiers .mo
    create_mo_file(english_translations, 'translations/en/LC_MESSAGES/messages.mo')
    print("✅ Anglais: translations/en/LC_MESSAGES/messages.mo")
    
    create_mo_file(spanish_translations, 'translations/es/LC_MESSAGES/messages.mo')
    print("✅ Espagnol: translations/es/LC_MESSAGES/messages.mo")
    
    create_mo_file(french_translations, 'translations/fr/LC_MESSAGES/messages.mo')
    print("✅ Français: translations/fr/LC_MESSAGES/messages.mo")
    
    print("✅ Tous les fichiers .mo ont été créés avec succès !")
