from flask import render_template, request, redirect, url_for, flash, session, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from flask_babel import _, get_locale
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from app import app, db
from models import User, Product, Order, OrderItem, Category
import os
from PIL import Image
from datetime import datetime

# Route pour changer de langue
@app.route('/set_language/<language>')
def set_language(language=None):
    if language in app.config['LANGUAGES']:
        session['language'] = language
    return redirect(request.referrer or url_for('index'))

# Routes principales
@app.route('/')
def index():
    featured_products = Product.query.filter_by(is_active=True).limit(8).all()
    categories = Category.query.all()
    return render_template('index.html', products=featured_products, categories=categories)

@app.route('/products')
def products():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    category_id = request.args.get('category', type=int)
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    
    query = Product.query.filter_by(is_active=True)
    
    if search:
        query = query.filter(Product.name.contains(search) | Product.description.contains(search))
    
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    if min_price:
        query = query.filter(Product.price >= min_price)
    
    if max_price:
        query = query.filter(Product.price <= max_price)
    
    products = query.paginate(page=page, per_page=12, error_out=False)
    categories = Category.query.all()
    
    return render_template('products.html', products=products, categories=categories,
                         search=search, selected_category=category_id,
                         min_price=min_price, max_price=max_price)

@app.route('/product/<int:id>')
def product_detail(id):
    product = Product.query.get_or_404(id)
    related_products = Product.query.filter(
        Product.category_id == product.category_id,
        Product.id != product.id,
        Product.is_active == True
    ).limit(4).all()
    
    return render_template('product_detail.html', product=product, related_products=related_products)

# Authentification
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            next_page = request.args.get('next')
            flash('Connexion réussie !', 'success')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Email ou mot de passe incorrect', 'error')
    
    return render_template('auth/login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # Vérifier si l'utilisateur existe déjà
        if User.query.filter_by(email=email).first():
            flash('Cet email est déjà utilisé', 'error')
            return render_template('auth/register.html')
        
        if User.query.filter_by(username=username).first():
            flash('Ce nom d\'utilisateur est déjà pris', 'error')
            return render_template('auth/register.html')
        
        # Créer le nouvel utilisateur
        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password)
        )
        
        db.session.add(user)
        db.session.commit()
        
        flash('Inscription réussie ! Vous pouvez maintenant vous connecter.', 'success')
        return redirect(url_for('login'))
    
    return render_template('auth/register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Vous avez été déconnecté', 'info')
    return redirect(url_for('index'))

# Panier et commandes
@app.route('/cart')
@login_required
def cart():
    cart_items = session.get('cart', {})
    products = []
    total = 0
    
    for product_id, quantity in cart_items.items():
        product = Product.query.get(int(product_id))
        if product:
            subtotal = product.price * quantity
            products.append({
                'product': product,
                'quantity': quantity,
                'subtotal': subtotal
            })
            total += subtotal
    
    return render_template('cart.html', cart_items=products, total=total)

@app.route('/add-to-cart', methods=['POST'])
@login_required
def add_to_cart():
    data = request.get_json()
    product_id = str(data.get('product_id'))
    quantity = int(data.get('quantity', 1))
    
    product = Product.query.get(int(product_id))
    if not product or not product.is_active:
        return jsonify({'success': False, 'message': 'Produit non trouvé'})
    
    if product.stock < quantity:
        return jsonify({'success': False, 'message': 'Stock insuffisant'})
    
    cart = session.get('cart', {})
    
    if product_id in cart:
        cart[product_id] += quantity
    else:
        cart[product_id] = quantity
    
    # Vérifier le stock total
    if cart[product_id] > product.stock:
        cart[product_id] = product.stock
        return jsonify({'success': False, 'message': f'Quantité ajustée au stock disponible ({product.stock})'})
    
    session['cart'] = cart
    return jsonify({'success': True})

@app.route('/cart-count')
@login_required
def cart_count():
    cart = session.get('cart', {})
    count = sum(cart.values())
    return jsonify({'count': count})

@app.route('/update-cart', methods=['POST'])
@login_required
def update_cart():
    data = request.get_json()
    product_id = str(data.get('product_id'))
    quantity = int(data.get('quantity', 0))
    
    cart = session.get('cart', {})
    
    if quantity <= 0:
        cart.pop(product_id, None)
    else:
        product = Product.query.get(int(product_id))
        if product and quantity <= product.stock:
            cart[product_id] = quantity
        else:
            return jsonify({'success': False, 'message': 'Stock insuffisant'})
    
    session['cart'] = cart
    return jsonify({'success': True})

@app.route('/remove-from-cart', methods=['POST'])
@login_required
def remove_from_cart():
    data = request.get_json()
    product_id = str(data.get('product_id'))

    cart = session.get('cart', {})
    cart.pop(product_id, None)
    session['cart'] = cart

    return jsonify({'success': True})

@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    cart = session.get('cart', {})
    if not cart:
        flash('Votre panier est vide', 'warning')
        return redirect(url_for('cart'))

    if request.method == 'POST':
        # Créer la commande
        total = 0
        order_items = []

        for product_id, quantity in cart.items():
            product = Product.query.get(int(product_id))
            if product and product.stock >= quantity:
                subtotal = product.price * quantity
                total += subtotal
                order_items.append({
                    'product': product,
                    'quantity': quantity,
                    'price': product.price
                })
            else:
                flash(f'Stock insuffisant pour {product.name}', 'error')
                return redirect(url_for('cart'))

        # Créer la commande
        order = Order(
            user_id=current_user.id,
            total_amount=total,
            shipping_address=request.form['address'],
            phone=request.form['phone']
        )
        db.session.add(order)
        db.session.flush()  # Pour obtenir l'ID de la commande

        # Ajouter les articles de commande
        for item in order_items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=item['product'].id,
                quantity=item['quantity'],
                price=item['price']
            )
            db.session.add(order_item)

            # Mettre à jour le stock
            item['product'].stock -= item['quantity']

        db.session.commit()

        # Vider le panier
        session.pop('cart', None)

        flash('Commande passée avec succès !', 'success')
        return redirect(url_for('order_confirmation', order_id=order.id))

    # Calculer le total pour l'affichage
    products = []
    total = 0

    for product_id, quantity in cart.items():
        product = Product.query.get(int(product_id))
        if product:
            subtotal = product.price * quantity
            products.append({
                'product': product,
                'quantity': quantity,
                'subtotal': subtotal
            })
            total += subtotal

    return render_template('checkout.html', cart_items=products, total=total)

@app.route('/order-confirmation/<int:order_id>')
@login_required
def order_confirmation(order_id):
    order = Order.query.filter_by(id=order_id, user_id=current_user.id).first_or_404()
    return render_template('order_confirmation.html', order=order)

@app.route('/orders')
@login_required
def orders():
    user_orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template('orders.html', orders=user_orders)

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

# Routes d'administration
@app.route('/admin')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        flash('Accès non autorisé', 'error')
        return redirect(url_for('index'))

    # Statistiques
    total_products = Product.query.count()
    total_orders = Order.query.count()
    total_users = User.query.count()
    pending_orders = Order.query.filter_by(status='pending').count()

    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(5).all()
    current_date = datetime.now().strftime('%d/%m/%Y')

    return render_template('admin/dashboard.html',
                         total_products=total_products,
                         total_orders=total_orders,
                         total_users=total_users,
                         pending_orders=pending_orders,
                         recent_orders=recent_orders,
                         current_date=current_date)

@app.route('/admin/products')
@login_required
def admin_products():
    if not current_user.is_admin:
        flash('Accès non autorisé', 'error')
        return redirect(url_for('index'))

    page = request.args.get('page', 1, type=int)
    products = Product.query.paginate(page=page, per_page=10, error_out=False)

    return render_template('admin/products.html', products=products)

@app.route('/admin/products/add', methods=['GET', 'POST'])
@login_required
def admin_add_product():
    if not current_user.is_admin:
        flash('Accès non autorisé', 'error')
        return redirect(url_for('index'))

    if request.method == 'POST':
        # Traitement de l'image
        image_filename = None
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename:
                filename = secure_filename(file.filename)
                # Ajouter un timestamp pour éviter les conflits
                import time
                filename = f"{int(time.time())}_{filename}"
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

                # Redimensionner l'image
                image = Image.open(file)
                image.thumbnail((500, 500), Image.Resampling.LANCZOS)
                image.save(file_path)
                image_filename = filename

        product = Product(
            name=request.form['name'],
            description=request.form['description'],
            price=float(request.form['price']),
            stock=int(request.form['stock']),
            brand=request.form['brand'],
            volume=request.form['volume'],
            gender=request.form['gender'],
            category_id=int(request.form['category_id']) if request.form['category_id'] else None,
            image_filename=image_filename
        )

        db.session.add(product)
        db.session.commit()

        flash('Produit ajouté avec succès !', 'success')
        return redirect(url_for('admin_products'))

    categories = Category.query.all()
    return render_template('admin/add_product.html', categories=categories)

@app.route('/admin/products/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_edit_product(id):
    if not current_user.is_admin:
        flash('Accès non autorisé', 'error')
        return redirect(url_for('index'))

    product = Product.query.get_or_404(id)

    if request.method == 'POST':
        # Traitement de l'image
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename:
                # Supprimer l'ancienne image
                if product.image_filename:
                    old_path = os.path.join(app.config['UPLOAD_FOLDER'], product.image_filename)
                    if os.path.exists(old_path):
                        os.remove(old_path)

                filename = secure_filename(file.filename)
                import time
                filename = f"{int(time.time())}_{filename}"
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

                image = Image.open(file)
                image.thumbnail((500, 500), Image.Resampling.LANCZOS)
                image.save(file_path)
                product.image_filename = filename

        product.name = request.form['name']
        product.description = request.form['description']
        product.price = float(request.form['price'])
        product.stock = int(request.form['stock'])
        product.brand = request.form['brand']
        product.volume = request.form['volume']
        product.gender = request.form['gender']
        product.category_id = int(request.form['category_id']) if request.form['category_id'] else None
        product.is_active = 'is_active' in request.form

        db.session.commit()

        flash('Produit modifié avec succès !', 'success')
        return redirect(url_for('admin_products'))

    categories = Category.query.all()
    return render_template('admin/edit_product.html', product=product, categories=categories)

@app.route('/admin/products/delete/<int:id>', methods=['POST'])
@login_required
def admin_delete_product(id):
    if not current_user.is_admin:
        flash('Accès non autorisé', 'error')
        return redirect(url_for('index'))

    product = Product.query.get_or_404(id)

    # Vérifier si le produit est référencé dans des commandes
    order_items_count = OrderItem.query.filter_by(product_id=product.id).count()
    if order_items_count > 0:
        flash(f'Impossible de supprimer ce produit car il est référencé dans {order_items_count} commande(s). Vous pouvez le désactiver à la place.', 'error')
        return redirect(url_for('admin_products'))

    # Supprimer l'image
    if product.image_filename:
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], product.image_filename)
        if os.path.exists(image_path):
            os.remove(image_path)

    try:
        db.session.delete(product)
        db.session.commit()
        flash('Produit supprimé avec succès !', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Erreur lors de la suppression du produit. Il est peut-être référencé dans des commandes.', 'error')

    return redirect(url_for('admin_products'))

@app.route('/admin/products/toggle/<int:id>', methods=['POST'])
@login_required
def admin_toggle_product(id):
    if not current_user.is_admin:
        flash('Accès non autorisé', 'error')
        return redirect(url_for('index'))

    product = Product.query.get_or_404(id)
    product.is_active = not product.is_active

    try:
        db.session.commit()
        status = 'activé' if product.is_active else 'désactivé'
        flash(f'Produit {status} avec succès !', 'success')
    except Exception:
        db.session.rollback()
        flash('Erreur lors de la modification du statut du produit.', 'error')

    return redirect(url_for('admin_products'))

@app.route('/admin/products/delete-all', methods=['POST'])
@login_required
def admin_delete_all_products():
    if not current_user.is_admin:
        flash('Accès non autorisé', 'error')
        return redirect(url_for('index'))

    try:
        # 1. Compter les produits avant suppression
        total_products = Product.query.count()

        if total_products == 0:
            flash('Aucun produit à supprimer.', 'info')
            return redirect(url_for('admin_products'))

        # 2. Récupérer les noms des images avant suppression
        products_with_images = Product.query.filter(Product.image_filename.isnot(None)).all()
        image_files = [product.image_filename for product in products_with_images]

        # 3. Supprimer tous les OrderItems (pour éviter les contraintes de clé étrangère)
        deleted_order_items = OrderItem.query.count()
        OrderItem.query.delete()

        # 4. Supprimer toutes les commandes
        deleted_orders = Order.query.count()
        Order.query.delete()

        # 5. Supprimer tous les produits
        Product.query.delete()

        # 6. Supprimer les images des produits
        deleted_images = 0
        images_path = os.path.join(app.static_folder, 'images', 'products')
        if os.path.exists(images_path):
            for image_filename in image_files:
                image_path = os.path.join(images_path, image_filename)
                if os.path.exists(image_path):
                    try:
                        os.remove(image_path)
                        deleted_images += 1
                    except Exception as e:
                        print(f"Erreur lors de la suppression de l'image {image_filename}: {e}")

        # 7. Sauvegarder les changements
        db.session.commit()

        # 8. Message de confirmation
        flash(f'✅ Suppression terminée avec succès ! {total_products} produits, {deleted_orders} commandes, {deleted_order_items} articles de commande et {deleted_images} images supprimés.', 'success')

    except Exception as e:
        db.session.rollback()
        flash(f'❌ Erreur lors de la suppression : {str(e)}', 'error')

    return redirect(url_for('admin_products'))

@app.route('/admin/orders')
@login_required
def admin_orders():
    if not current_user.is_admin:
        flash('Accès non autorisé', 'error')
        return redirect(url_for('index'))

    page = request.args.get('page', 1, type=int)
    status_filter = request.args.get('status', '')

    query = Order.query
    if status_filter:
        query = query.filter_by(status=status_filter)

    orders = query.order_by(Order.created_at.desc()).paginate(page=page, per_page=10, error_out=False)

    return render_template('admin/orders.html', orders=orders, status_filter=status_filter)

@app.route('/admin/orders/<int:id>')
@login_required
def admin_order_detail(id):
    if not current_user.is_admin:
        flash('Accès non autorisé', 'error')
        return redirect(url_for('index'))

    order = Order.query.get_or_404(id)
    return render_template('admin/order_detail.html', order=order)

@app.route('/admin/orders/<int:id>/update-status', methods=['POST'])
@login_required
def admin_update_order_status(id):
    if not current_user.is_admin:
        flash('Accès non autorisé', 'error')
        return redirect(url_for('index'))

    order = Order.query.get_or_404(id)
    new_status = request.form['status']

    if new_status in ['pending', 'confirmed', 'shipped', 'delivered', 'cancelled']:
        order.status = new_status
        db.session.commit()
        flash('Statut de la commande mis à jour !', 'success')
    else:
        flash('Statut invalide', 'error')

    return redirect(url_for('admin_order_detail', id=id))

@app.route('/admin/categories')
@login_required
def admin_categories():
    if not current_user.is_admin:
        flash('Accès non autorisé', 'error')
        return redirect(url_for('index'))

    categories = Category.query.all()
    return render_template('admin/categories.html', categories=categories)

@app.route('/admin/categories/add', methods=['GET', 'POST'])
@login_required
def admin_add_category():
    if not current_user.is_admin:
        flash('Accès non autorisé', 'error')
        return redirect(url_for('index'))

    if request.method == 'POST':
        category = Category(
            name=request.form['name'],
            description=request.form['description']
        )

        db.session.add(category)
        db.session.commit()

        flash('Catégorie ajoutée avec succès !', 'success')
        return redirect(url_for('admin_categories'))

    return render_template('admin/add_category.html')

@app.route('/admin/categories/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_edit_category(id):
    if not current_user.is_admin:
        flash('Accès non autorisé', 'error')
        return redirect(url_for('index'))

    category = Category.query.get_or_404(id)

    if request.method == 'POST':
        category.name = request.form['name']
        category.description = request.form['description']

        db.session.commit()

        flash('Catégorie modifiée avec succès !', 'success')
        return redirect(url_for('admin_categories'))

    return render_template('admin/edit_category.html', category=category)

@app.route('/admin/categories/delete/<int:id>', methods=['POST'])
@login_required
def admin_delete_category(id):
    if not current_user.is_admin:
        flash('Accès non autorisé', 'error')
        return redirect(url_for('index'))

    category = Category.query.get_or_404(id)

    # Vérifier s'il y a des produits dans cette catégorie
    if category.products:
        flash('Impossible de supprimer une catégorie contenant des produits', 'error')
        return redirect(url_for('admin_categories'))

    db.session.delete(category)
    db.session.commit()

    flash('Catégorie supprimée avec succès !', 'success')
    return redirect(url_for('admin_categories'))

# Routes de gestion des utilisateurs
@app.route('/admin/users')
@login_required
def admin_users():
    if not current_user.is_admin:
        flash('Accès non autorisé', 'error')
        return redirect(url_for('index'))

    page = request.args.get('page', 1, type=int)
    filter_type = request.args.get('filter', '')

    query = User.query

    if filter_type == 'admin':
        query = query.filter_by(is_admin=True)
    elif filter_type == 'regular':
        query = query.filter_by(is_admin=False)

    users = query.order_by(User.created_at.desc()).paginate(page=page, per_page=10, error_out=False)

    # Statistiques
    admin_count = User.query.filter_by(is_admin=True).count()
    users_with_orders = User.query.join(Order).distinct().count()

    # Utilisateurs récents (7 derniers jours)
    from datetime import datetime, timedelta
    week_ago = datetime.utcnow() - timedelta(days=7)
    recent_users = User.query.filter(User.created_at >= week_ago).count()

    return render_template('admin/users.html',
                         users=users,
                         admin_count=admin_count,
                         users_with_orders=users_with_orders,
                         recent_users=recent_users)

@app.route('/admin/users/<int:id>')
@login_required
def admin_user_detail(id):
    if not current_user.is_admin:
        flash('Accès non autorisé', 'error')
        return redirect(url_for('index'))

    user = User.query.get_or_404(id)

    # Calculer le nombre de jours depuis l'inscription
    from datetime import datetime
    days_since_registration = (datetime.utcnow() - user.created_at).days

    return render_template('admin/user_detail.html',
                         user=user,
                         days_since_registration=days_since_registration)

@app.route('/admin/users/<int:id>/toggle-admin', methods=['POST'])
@login_required
def admin_toggle_user_admin(id):
    if not current_user.is_admin:
        flash('Accès non autorisé', 'error')
        return redirect(url_for('index'))

    user = User.query.get_or_404(id)

    # Empêcher de se retirer ses propres droits admin
    if user.id == current_user.id:
        flash('Vous ne pouvez pas modifier vos propres droits administrateur.', 'error')
        return redirect(url_for('admin_users'))

    try:
        user.is_admin = not user.is_admin
        db.session.commit()

        action = 'promu administrateur' if user.is_admin else 'retiré des administrateurs'
        flash(f'L\'utilisateur {user.username} a été {action} avec succès !', 'success')

    except Exception as e:
        db.session.rollback()
        flash(f'Erreur lors de la modification : {str(e)}', 'error')

    return redirect(url_for('admin_users'))

@app.route('/admin/users/<int:id>/delete', methods=['POST'])
@login_required
def admin_delete_user(id):
    if not current_user.is_admin:
        flash('Accès non autorisé', 'error')
        return redirect(url_for('index'))

    user = User.query.get_or_404(id)

    # Empêcher de se supprimer soi-même
    if user.id == current_user.id:
        flash('Vous ne pouvez pas supprimer votre propre compte.', 'error')
        return redirect(url_for('admin_users'))

    try:
        # Statistiques avant suppression
        orders_count = len(user.orders)
        total_spent = sum(order.total_amount for order in user.orders)

        # 1. Supprimer tous les OrderItems liés aux commandes de cet utilisateur
        deleted_order_items = 0
        for order in user.orders:
            deleted_order_items += len(order.items)
            # Supprimer les OrderItems de cette commande
            OrderItem.query.filter_by(order_id=order.id).delete()

        # 2. Supprimer toutes les commandes de cet utilisateur
        Order.query.filter_by(user_id=user.id).delete()

        # 3. Supprimer l'utilisateur
        username = user.username
        email = user.email
        db.session.delete(user)

        # 4. Sauvegarder les changements
        db.session.commit()

        # 5. Message de confirmation
        if orders_count > 0:
            flash(f'✅ Utilisateur {username} ({email}) supprimé avec succès ! '
                  f'{orders_count} commandes, {deleted_order_items} articles de commande '
                  f'et {total_spent:.2f}€ de données supprimées.', 'success')
        else:
            flash(f'✅ Utilisateur {username} ({email}) supprimé avec succès !', 'success')

    except Exception as e:
        db.session.rollback()
        flash(f'❌ Erreur lors de la suppression : {str(e)}', 'error')

    return redirect(url_for('admin_users'))
