#!/usr/bin/env python3
"""
Script d'initialisation de la base de données avec des données de test
"""

from app import app, db
from models import User, Product, Category, Order, OrderItem
from werkzeug.security import generate_password_hash
from datetime import datetime

def init_database():
    """Initialise la base de données avec des données de test"""
    
    with app.app_context():
        # Supprimer toutes les tables existantes et les recréer
        db.drop_all()
        db.create_all()
        
        print("Base de données initialisée...")
        
        # Créer l'utilisateur admin
        admin = User(
            username='admin',
            email='admin@velours-parfum.com',
            password_hash=generate_password_hash('admin123'),
            is_admin=True
        )
        db.session.add(admin)
        
        # Créer quelques utilisateurs de test
        users = [
            User(
                username='jean_dupont',
                email='jean.dupont@email.com',
                password_hash=generate_password_hash('password123')
            ),
            User(
                username='marie_martin',
                email='marie.martin@email.com',
                password_hash=generate_password_hash('password123')
            ),
            User(
                username='pierre_durand',
                email='pierre.durand@email.com',
                password_hash=generate_password_hash('password123')
            )
        ]
        
        for user in users:
            db.session.add(user)
        
        print("Utilisateurs créés...")
        
        # Créer les catégories
        categories = [
            Category(
                name='Parfums pour Homme',
                description='Collection de parfums masculins élégants et raffinés'
            ),
            Category(
                name='Parfums pour Femme',
                description='Fragrances féminines délicates et envoûtantes'
            ),
            Category(
                name='Parfums Mixtes',
                description='Parfums unisexes pour tous les goûts'
            ),
            Category(
                name='Eaux de Toilette',
                description='Fragrances légères pour un usage quotidien'
            ),
            Category(
                name='Parfums de Luxe',
                description='Collection premium de parfums d\'exception'
            )
        ]
        
        for category in categories:
            db.session.add(category)
        
        db.session.commit()  # Commit pour obtenir les IDs des catégories
        
        print("Catégories créées...")
        
        # Créer les produits de test
        products = [
            # Parfums pour Homme
            Product(
                name='Dior Sauvage',
                description='Un parfum masculin frais et épicé aux notes de bergamote et de poivre. Parfait pour l\'homme moderne et élégant.',
                price=89.99,
                stock=25,
                brand='Dior',
                volume='100ml',
                gender='homme',
                category_id=1,
                is_active=True
            ),
            Product(
                name='Chanel Bleu de Chanel',
                description='Une fragrance boisée aromatique qui exprime la liberté avec un caractère déterminé et un esprit indépendant.',
                price=95.50,
                stock=18,
                brand='Chanel',
                volume='100ml',
                gender='homme',
                category_id=1,
                is_active=True
            ),
            Product(
                name='Tom Ford Oud Wood',
                description='Un parfum oriental boisé sophistiqué avec des notes de bois de oud, palissandre et santal.',
                price=245.00,
                stock=8,
                brand='Tom Ford',
                volume='50ml',
                gender='homme',
                category_id=5,
                is_active=True
            ),
            
            # Parfums pour Femme
            Product(
                name='Chanel N°5',
                description='Le parfum le plus célèbre au monde. Un bouquet floral aldéhydé intemporel et élégant.',
                price=125.00,
                stock=30,
                brand='Chanel',
                volume='100ml',
                gender='femme',
                category_id=2,
                is_active=True
            ),
            Product(
                name='Dior J\'adore',
                description='Un parfum floral moderne et féminin aux notes de ylang-ylang, rose de Damas et jasmin.',
                price=98.00,
                stock=22,
                brand='Dior',
                volume='100ml',
                gender='femme',
                category_id=2,
                is_active=True
            ),
            Product(
                name='Yves Saint Laurent Black Opium',
                description='Un parfum gourmand et addictif aux notes de café noir, vanille et fleur d\'oranger.',
                price=87.50,
                stock=15,
                brand='YSL',
                volume='90ml',
                gender='femme',
                category_id=2,
                is_active=True
            ),
            
            # Parfums Mixtes
            Product(
                name='Hermès Terre d\'Hermès',
                description='Un parfum minéral et boisé qui raconte la relation de l\'homme à la terre.',
                price=105.00,
                stock=20,
                brand='Hermès',
                volume='100ml',
                gender='mixte',
                category_id=3,
                is_active=True
            ),
            Product(
                name='Maison Margiela Replica Beach Walk',
                description='Une fragrance qui évoque une promenade sur la plage avec des notes salées et ensoleillées.',
                price=78.00,
                stock=12,
                brand='Maison Margiela',
                volume='100ml',
                gender='mixte',
                category_id=3,
                is_active=True
            ),
            
            # Eaux de Toilette
            Product(
                name='Eau de Toilette Citrus Fresh',
                description='Une eau de toilette rafraîchissante aux agrumes pour un réveil tonique.',
                price=35.00,
                stock=45,
                brand='Fresh & Co',
                volume='100ml',
                gender='mixte',
                category_id=4,
                is_active=True
            ),
            Product(
                name='Lavande de Provence EDT',
                description='Une eau de toilette délicate aux notes de lavande authentique de Provence.',
                price=42.00,
                stock=28,
                brand='Provence Parfums',
                volume='100ml',
                gender='mixte',
                category_id=4,
                is_active=True
            ),
            
            # Parfums de Luxe
            Product(
                name='Creed Aventus',
                description='Un parfum de luxe fruité et fumé, symbole de force, de vision et de succès.',
                price=320.00,
                stock=5,
                brand='Creed',
                volume='100ml',
                gender='homme',
                category_id=5,
                is_active=True
            ),
            Product(
                name='Clive Christian No. 1',
                description='L\'un des parfums les plus chers au monde, une création d\'exception aux ingrédients rares.',
                price=450.00,
                stock=3,
                brand='Clive Christian',
                volume='50ml',
                gender='mixte',
                category_id=5,
                is_active=True
            )
        ]
        
        for product in products:
            db.session.add(product)
        
        db.session.commit()
        
        print("Produits créés...")
        
        # Créer quelques commandes de test
        orders = [
            Order(
                user_id=2,  # jean_dupont
                total_amount=184.99,
                status='delivered',
                shipping_address='123 Rue de la Paix, 75001 Paris',
                phone='01 23 45 67 89',
                created_at=datetime(2024, 1, 15, 10, 30)
            ),
            Order(
                user_id=3,  # marie_martin
                total_amount=125.00,
                status='shipped',
                shipping_address='456 Avenue des Champs, 69000 Lyon',
                phone='04 56 78 90 12',
                created_at=datetime(2024, 1, 20, 14, 45)
            ),
            Order(
                user_id=4,  # pierre_durand
                total_amount=87.50,
                status='pending',
                shipping_address='789 Boulevard Saint-Michel, 13000 Marseille',
                phone='04 91 23 45 67',
                created_at=datetime(2024, 1, 25, 16, 20)
            )
        ]
        
        for order in orders:
            db.session.add(order)
        
        db.session.commit()
        
        # Créer les articles de commande
        order_items = [
            # Commande 1
            OrderItem(order_id=1, product_id=1, quantity=2, price=89.99),  # Dior Sauvage x2
            OrderItem(order_id=1, product_id=9, quantity=1, price=35.00),  # Citrus Fresh x1
            
            # Commande 2
            OrderItem(order_id=2, product_id=4, quantity=1, price=125.00),  # Chanel N°5 x1
            
            # Commande 3
            OrderItem(order_id=3, product_id=6, quantity=1, price=87.50),  # YSL Black Opium x1
        ]
        
        for item in order_items:
            db.session.add(item)
        
        db.session.commit()
        
        print("Commandes de test créées...")
        print("\n" + "="*50)
        print("INITIALISATION TERMINÉE !")
        print("="*50)
        print("\nCompte administrateur créé :")
        print("Email: admin@parfume.com")
        print("Mot de passe: admin123")
        print("\nComptes utilisateurs de test :")
        print("- jean.dupont@email.com / password123")
        print("- marie.martin@email.com / password123")
        print("- pierre.durand@email.com / password123")
        print("\nDonnées créées :")
        print(f"- {len(categories)} catégories")
        print(f"- {len(products)} produits")
        print(f"- {len(users) + 1} utilisateurs")
        print(f"- {len(orders)} commandes de test")
        print("\nVous pouvez maintenant lancer l'application avec: python app.py")

if __name__ == '__main__':
    init_database()
