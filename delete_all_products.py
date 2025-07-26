#!/usr/bin/env python3
"""
Script pour supprimer tous les produits disponibles
"""

import sqlite3
import os
import shutil

def delete_all_products():
    """Supprime tous les produits de la base de données"""
    
    db_path = 'instance/velours_parfum.db'
    images_path = 'static/images/products'
    
    if not os.path.exists(db_path):
        print("❌ Base de données non trouvée")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🗑️ Suppression de tous les produits...")
        
        # 1. Vérifier combien de produits existent
        cursor.execute("SELECT COUNT(*) FROM product")
        total_products = cursor.fetchone()[0]
        print(f"📊 Nombre total de produits : {total_products}")
        
        if total_products == 0:
            print("✅ Aucun produit à supprimer")
            conn.close()
            return True
        
        # 2. Vérifier les produits référencés dans des commandes
        cursor.execute("""
            SELECT COUNT(DISTINCT product_id) 
            FROM order_item 
            WHERE product_id IN (SELECT id FROM product)
        """)
        referenced_products = cursor.fetchone()[0]
        print(f"⚠️  Produits référencés dans des commandes : {referenced_products}")
        
        # 3. Supprimer d'abord tous les OrderItems (pour éviter les contraintes)
        cursor.execute("SELECT COUNT(*) FROM order_item")
        total_order_items = cursor.fetchone()[0]
        
        if total_order_items > 0:
            print(f"🗑️ Suppression de {total_order_items} articles de commande...")
            cursor.execute("DELETE FROM order_item")
            print("✅ Articles de commande supprimés")
        
        # 4. Supprimer toutes les commandes vides
        cursor.execute("SELECT COUNT(*) FROM 'order'")
        total_orders = cursor.fetchone()[0]
        
        if total_orders > 0:
            print(f"🗑️ Suppression de {total_orders} commandes...")
            cursor.execute("DELETE FROM 'order'")
            print("✅ Commandes supprimées")
        
        # 5. Récupérer les noms des images avant suppression
        cursor.execute("SELECT image_filename FROM product WHERE image_filename IS NOT NULL")
        image_files = [row[0] for row in cursor.fetchall()]
        
        # 6. Supprimer tous les produits
        cursor.execute("DELETE FROM product")
        deleted_products = cursor.rowcount
        print(f"✅ {deleted_products} produits supprimés de la base de données")
        
        # 7. Supprimer les images des produits
        if image_files and os.path.exists(images_path):
            deleted_images = 0
            for image_file in image_files:
                image_path = os.path.join(images_path, image_file)
                if os.path.exists(image_path):
                    try:
                        os.remove(image_path)
                        deleted_images += 1
                    except Exception as e:
                        print(f"⚠️  Impossible de supprimer l'image {image_file}: {e}")
            
            print(f"🖼️ {deleted_images} images supprimées")
        
        # 8. Réinitialiser les compteurs auto-increment
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='product'")
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='order'")
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='order_item'")
        
        # 9. Statistiques finales
        cursor.execute("SELECT COUNT(*) FROM user")
        users_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM category")
        categories_count = cursor.fetchone()[0]
        
        print(f"\n📊 Statistiques après suppression :")
        print(f"   - Utilisateurs : {users_count}")
        print(f"   - Produits : 0")
        print(f"   - Catégories : {categories_count}")
        print(f"   - Commandes : 0")
        print(f"   - Articles de commande : 0")
        
        # Sauvegarder les changements
        conn.commit()
        conn.close()
        
        print("\n✅ Tous les produits ont été supprimés avec succès !")
        print("⚠️  Note: Toutes les commandes ont également été supprimées pour éviter les erreurs d'intégrité")
        return True
        
    except Exception as e:
        print(f"❌ Erreur : {e}")
        if 'conn' in locals():
            conn.rollback()
            conn.close()
        return False

def delete_products_only():
    """Supprime uniquement les produits non référencés dans des commandes"""
    
    db_path = 'instance/velours_parfum.db'
    images_path = 'static/images/products'
    
    if not os.path.exists(db_path):
        print("❌ Base de données non trouvée")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🗑️ Suppression des produits non référencés...")
        
        # 1. Identifier les produits non référencés
        cursor.execute("""
            SELECT id, image_filename FROM product 
            WHERE id NOT IN (SELECT DISTINCT product_id FROM order_item WHERE product_id IS NOT NULL)
        """)
        unreferenced_products = cursor.fetchall()
        
        if not unreferenced_products:
            print("✅ Aucun produit non référencé à supprimer")
            conn.close()
            return True
        
        print(f"📊 Produits non référencés trouvés : {len(unreferenced_products)}")
        
        # 2. Supprimer les images
        deleted_images = 0
        for product_id, image_filename in unreferenced_products:
            if image_filename and os.path.exists(images_path):
                image_path = os.path.join(images_path, image_filename)
                if os.path.exists(image_path):
                    try:
                        os.remove(image_path)
                        deleted_images += 1
                    except Exception as e:
                        print(f"⚠️  Impossible de supprimer l'image {image_filename}: {e}")
        
        # 3. Supprimer les produits non référencés
        cursor.execute("""
            DELETE FROM product 
            WHERE id NOT IN (SELECT DISTINCT product_id FROM order_item WHERE product_id IS NOT NULL)
        """)
        deleted_products = cursor.rowcount
        
        print(f"✅ {deleted_products} produits supprimés")
        print(f"🖼️ {deleted_images} images supprimées")
        
        # 4. Vérifier les produits restants
        cursor.execute("SELECT COUNT(*) FROM product")
        remaining_products = cursor.fetchone()[0]
        print(f"📊 Produits restants (référencés dans des commandes) : {remaining_products}")
        
        conn.commit()
        conn.close()
        
        print("\n✅ Suppression terminée !")
        return True
        
    except Exception as e:
        print(f"❌ Erreur : {e}")
        if 'conn' in locals():
            conn.rollback()
            conn.close()
        return False

if __name__ == '__main__':
    import sys
    
    print("🗑️ SUPPRESSION DES PRODUITS")
    print("=" * 50)
    print("1. Supprimer TOUS les produits (et toutes les commandes)")
    print("2. Supprimer uniquement les produits non référencés")
    print("3. Annuler")
    
    choice = input("\nVotre choix (1/2/3) : ").strip()
    
    if choice == '1':
        print("\n⚠️  ATTENTION : Cette opération va supprimer TOUS les produits ET toutes les commandes !")
        confirm = input("Tapez 'DELETE ALL' pour confirmer : ")
        if confirm == 'DELETE ALL':
            delete_all_products()
        else:
            print("❌ Opération annulée")
    
    elif choice == '2':
        print("\n⚠️  Cette opération va supprimer les produits non référencés dans des commandes")
        confirm = input("Tapez 'DELETE' pour confirmer : ")
        if confirm == 'DELETE':
            delete_products_only()
        else:
            print("❌ Opération annulée")
    
    elif choice == '3':
        print("❌ Opération annulée")
    
    else:
        print("❌ Choix invalide")
