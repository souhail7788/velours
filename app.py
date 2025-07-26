from flask import Flask, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_babel import Babel, get_locale
from werkzeug.security import generate_password_hash
import os
import secrets

app = Flask(__name__)

# Configuration pour la production et le développement
if os.environ.get('RAILWAY_ENVIRONMENT'):
    # Configuration pour Railway (production)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', secrets.token_hex(16))
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///velours_parfum.db')
    app.config['DEBUG'] = False
else:
    # Configuration pour le développement local
    app.config['SECRET_KEY'] = secrets.token_hex(16)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///velours_parfum.db'
    app.config['DEBUG'] = True

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/images/products'

# Configuration multilingue
app.config['LANGUAGES'] = {
    'fr': 'Français',
    'en': 'English',
    'es': 'Español'
}
app.config['BABEL_DEFAULT_LOCALE'] = 'fr'
app.config['BABEL_DEFAULT_TIMEZONE'] = 'UTC'

# Créer le dossier d'upload s'il n'existe pas
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db = SQLAlchemy(app)
babel = Babel()
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Veuillez vous connecter pour accéder à cette page.'

@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(int(user_id))

def get_locale():
    # 1. Si une langue est forcée dans l'URL
    if request.args.get('lang'):
        session['language'] = request.args.get('lang')

    # 2. Si une langue est en session
    if 'language' in session:
        return session['language']

    # 3. Sinon, utiliser la langue préférée du navigateur
    return request.accept_languages.best_match(app.config['LANGUAGES'].keys()) or app.config['BABEL_DEFAULT_LOCALE']

# Configurer Babel avec le sélecteur de locale
def configure_babel():
    babel.init_app(app)

    # Fonction de sélection de locale pour Flask-Babel 4.0
    def locale_selector():
        return get_locale()

    # Assigner le sélecteur
    babel.locale_selector_func = locale_selector

configure_babel()

# Dictionnaire de traductions simple
TRANSLATIONS = {
    'en': {
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
        "Votre destination pour les parfums de luxe": "Your destination for luxury perfumes",
        "Tous droits réservés.": "All rights reserved.",
        # Admin interface
        "Dashboard": "Dashboard",
        "Admin Panel": "Admin Panel",
        "Voir le site": "View site",
        "Commandes": "Orders",
        "Utilisateurs": "Users",
        "Catégories": "Categories",
        "Total Produits": "Total Products",
        "Total Commandes": "Total Orders",
        "Total Utilisateurs": "Total Users",
        "Commandes en attente": "Pending Orders",
        "Commandes récentes": "Recent Orders",
        "Actions rapides": "Quick Actions",
        "Informations système": "System Information",
        "Ajouter un produit": "Add Product",
        "Ajouter une catégorie": "Add Category",
        "Voir les commandes en attente": "View Pending Orders",
        "Version": "Version",
        "Dernière mise à jour": "Last Update",
        "Statut": "Status",
        "Opérationnel": "Operational",
        "Gestion des produits": "Product Management",
        "Gestion des utilisateurs": "User Management",
        "Supprimer tous les produits": "Delete All Products",
        "Filtrer": "Filter",
        "Tous les utilisateurs": "All Users",
        "Administrateurs": "Administrators",
        "Utilisateurs réguliers": "Regular Users",
        "Nom d'utilisateur": "Username",
        "Email": "Email",
        "Type": "Type",
        "Date d'inscription": "Registration Date",
        "Total dépensé": "Total Spent",
        "Actions": "Actions",
        "Administrateur": "Administrator",
        "Utilisateur": "User",
        "commande(s)": "order(s)",
        "Voir détails": "View Details",
        "Retirer admin": "Remove Admin",
        "Promouvoir admin": "Promote Admin",
        "Supprimer": "Delete",
        "Retour à la liste": "Back to List",
        "Imprimer": "Print",
        "Articles commandés": "Ordered Items",
        "Produit": "Product",
        "Prix unitaire": "Unit Price",
        "Quantité": "Quantity",
        "Total": "Total",
        "Exporter": "Export",
        "Aucune commande récente": "No recent orders",
        "En attente": "Pending",
        "Confirmée": "Confirmed",
        "Expédiée": "Shipped",
        "Livrée": "Delivered",
        "Annulée": "Cancelled",
        "Voir toutes les commandes": "View All Orders",
        "Client": "Customer",
        "Date": "Date",
        "Accès non autorisé": "Unauthorized access",
        "Vous ne pouvez pas modifier vos propres droits administrateur.": "You cannot modify your own administrator rights.",
        "Vous ne pouvez pas supprimer votre propre compte.": "You cannot delete your own account.",
        "promu administrateur": "promoted to administrator",
        "retiré des administrateurs": "removed from administrators",
        "L'utilisateur {username} a été {action} avec succès !": "User {username} has been {action} successfully!",
        "Erreur lors de la modification : {error}": "Error during modification: {error}",
        "Utilisateur supprimé avec succès": "User deleted successfully",
        "Erreur lors de la suppression : {error}": "Error during deletion: {error}"
    },
    'es': {
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
        "Votre destination pour les parfums de luxe": "Tu destino para perfumes de lujo",
        "Tous droits réservés.": "Todos los derechos reservados.",
        # Admin interface
        "Dashboard": "Panel de Control",
        "Admin Panel": "Panel de Administración",
        "Voir le site": "Ver sitio",
        "Commandes": "Pedidos",
        "Utilisateurs": "Usuarios",
        "Catégories": "Categorías",
        "Total Produits": "Total Productos",
        "Total Commandes": "Total Pedidos",
        "Total Utilisateurs": "Total Usuarios",
        "Commandes en attente": "Pedidos Pendientes",
        "Commandes récentes": "Pedidos Recientes",
        "Actions rapides": "Acciones Rápidas",
        "Informations système": "Información del Sistema",
        "Ajouter un produit": "Añadir Producto",
        "Ajouter une catégorie": "Añadir Categoría",
        "Voir les commandes en attente": "Ver Pedidos Pendientes",
        "Version": "Versión",
        "Dernière mise à jour": "Última Actualización",
        "Statut": "Estado",
        "Opérationnel": "Operacional",
        "Gestion des produits": "Gestión de Productos",
        "Gestion des utilisateurs": "Gestión de Usuarios",
        "Supprimer tous les produits": "Eliminar Todos los Productos",
        "Filtrer": "Filtrar",
        "Tous les utilisateurs": "Todos los Usuarios",
        "Administrateurs": "Administradores",
        "Utilisateurs réguliers": "Usuarios Regulares",
        "Nom d'utilisateur": "Nombre de Usuario",
        "Email": "Email",
        "Type": "Tipo",
        "Date d'inscription": "Fecha de Registro",
        "Total dépensé": "Total Gastado",
        "Actions": "Acciones",
        "Administrateur": "Administrador",
        "Utilisateur": "Usuario",
        "commande(s)": "pedido(s)",
        "Voir détails": "Ver Detalles",
        "Retirer admin": "Quitar Admin",
        "Promouvoir admin": "Promover Admin",
        "Supprimer": "Eliminar",
        "Retour à la liste": "Volver a la Lista",
        "Imprimer": "Imprimir",
        "Articles commandés": "Artículos Pedidos",
        "Produit": "Producto",
        "Prix unitaire": "Precio Unitario",
        "Quantité": "Cantidad",
        "Total": "Total",
        "Exporter": "Exportar",
        "Aucune commande récente": "No hay pedidos recientes",
        "En attente": "Pendiente",
        "Confirmée": "Confirmado",
        "Expédiée": "Enviado",
        "Livrée": "Entregado",
        "Annulée": "Cancelado",
        "Voir toutes les commandes": "Ver Todos los Pedidos",
        "Client": "Cliente",
        "Date": "Fecha",
        "Accès non autorisé": "Acceso no autorizado",
        "Vous ne pouvez pas modifier vos propres droits administrateur.": "No puedes modificar tus propios derechos de administrador.",
        "Vous ne pouvez pas supprimer votre propre compte.": "No puedes eliminar tu propia cuenta.",
        "promu administrateur": "promovido a administrador",
        "retiré des administrateurs": "retirado de administradores",
        "L'utilisateur {username} a été {action} avec succès !": "¡El usuario {username} ha sido {action} con éxito!",
        "Erreur lors de la modification : {error}": "Error durante la modificación: {error}",
        "Utilisateur supprimé avec succès": "Usuario eliminado con éxito",
        "Erreur lors de la suppression : {error}": "Error durante la eliminación: {error}"
    },
    'fr': {}  # Français = texte original
}

# Fonction de traduction personnalisée
def custom_gettext(text):
    try:
        # Vérifier directement la session
        if 'language' in session:
            locale = session['language']
        else:
            locale = request.accept_languages.best_match(app.config['LANGUAGES'].keys()) or 'fr'

        if locale in TRANSLATIONS and text in TRANSLATIONS[locale]:
            return TRANSLATIONS[locale][text]
    except Exception:
        pass
    return text

# Rendre les fonctions de traduction disponibles dans tous les templates
@app.context_processor
def inject_conf_vars():
    return {
        '_': custom_gettext,
        'get_locale': get_locale,
        'LANGUAGES': app.config['LANGUAGES']
    }

def init_db():
    """Initialise la base de données et crée l'admin par défaut"""
    # Import ici pour éviter les imports circulaires
    from models import User

    with app.app_context():
        db.create_all()
        # Créer un admin par défaut
        admin = User.query.filter_by(email='admin@velours-parfum.com').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@velours-parfum.com',
                password_hash=generate_password_hash('admin123'),
                is_admin=True
            )
            db.session.add(admin)
            db.session.commit()

# Import des modèles et routes ici pour éviter les imports circulaires
from models import User, Product, Order, OrderItem, Category
from routes import *

# Initialiser la base de données
init_db()

if __name__ == '__main__':
    # Pour le développement local uniquement
    app.run(debug=True, port=5001)
