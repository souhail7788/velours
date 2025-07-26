#!/usr/bin/env python3
"""
Script simple pour corriger la base de données sans imports circulaires
"""

import sqlite3
import os

def fix_database_simple():
    """Corrige directement la base de données SQLite"""
    
    db_path = 'instance/velours_parfum.db'
    
    if not os.path.exists(db_path):
        print("❌ Base de données non trouvée")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🔧 Correction de la base de données...")
        
        # 1. Supprimer les OrderItems orphelins (product_id NULL)
        cursor.execute("DELETE FROM order_item WHERE product_id IS NULL")
        deleted_null = cursor.rowcount
        if deleted_null > 0:
            print(f"✅ Supprimé {deleted_null} OrderItems avec product_id NULL")
        
        # 2. Supprimer les OrderItems avec des product_id invalides
        cursor.execute("""
            DELETE FROM order_item 
            WHERE product_id NOT IN (SELECT id FROM product)
        """)
        deleted_invalid = cursor.rowcount
        if deleted_invalid > 0:
            print(f"✅ Supprimé {deleted_invalid} OrderItems avec product_id invalide")
        
        # 3. Supprimer les commandes vides
        cursor.execute("""
            DELETE FROM "order" 
            WHERE id NOT IN (SELECT DISTINCT order_id FROM order_item)
        """)
        deleted_orders = cursor.rowcount
        if deleted_orders > 0:
            print(f"✅ Supprimé {deleted_orders} commandes vides")
        
        # 4. Statistiques finales
        cursor.execute("SELECT COUNT(*) FROM user")
        users_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM product")
        products_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM category")
        categories_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM 'order'")
        orders_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM order_item")
        order_items_count = cursor.fetchone()[0]
        
        print(f"\n📊 Statistiques finales :")
        print(f"   - Utilisateurs : {users_count}")
        print(f"   - Produits : {products_count}")
        print(f"   - Catégories : {categories_count}")
        print(f"   - Commandes : {orders_count}")
        print(f"   - Articles de commande : {order_items_count}")
        
        # Sauvegarder les changements
        conn.commit()
        conn.close()
        
        print("\n✅ Base de données corrigée avec succès !")
        return True
        
    except Exception as e:
        print(f"❌ Erreur : {e}")
        return False

if __name__ == '__main__':
    fix_database_simple()
