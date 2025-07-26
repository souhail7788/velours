// Modern Parfume Store JavaScript with Enhanced UX

document.addEventListener('DOMContentLoaded', function() {
    // Initialize modern features
    initModernFeatures();
    updateCartCount();

    // Add to cart functionality with modern animations
    const addToCartButtons = document.querySelectorAll('.add-to-cart');
    addToCartButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const productId = this.dataset.productId;
            const quantity = this.dataset.quantity || 1;

            // Add loading animation
            this.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Ajout...';
            this.disabled = true;

            addToCart(productId, quantity, this);
        });
    });

    // Quantity update in cart
    const quantityInputs = document.querySelectorAll('.quantity-input');
    quantityInputs.forEach(input => {
        input.addEventListener('change', function() {
            const productId = this.dataset.productId;
            const quantity = this.value;

            updateCartQuantity(productId, quantity);
        });
    });

    // Remove from cart
    const removeButtons = document.querySelectorAll('.remove-from-cart');
    removeButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const productId = this.dataset.productId;

            removeFromCart(productId);
        });
    });
});

// Initialize modern features
function initModernFeatures() {
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Add scroll effect to navbar
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        window.addEventListener('scroll', function() {
            if (window.scrollY > 50) {
                navbar.style.background = 'rgba(255, 255, 255, 0.98)';
                navbar.style.boxShadow = '0 4px 20px rgba(0,0,0,0.1)';
            } else {
                navbar.style.background = 'rgba(255, 255, 255, 0.95)';
                navbar.style.boxShadow = '0 2px 4px rgba(0,0,0,0.1)';
            }
        });
    }

    // Add intersection observer for animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // Observe product cards for animation
    document.querySelectorAll('.product-card').forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(card);
    });
}

// Add product to cart with modern animations
function addToCart(productId, quantity = 1, button = null) {
    fetch('/add-to-cart', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            product_id: productId,
            quantity: quantity
        })
    })
    .then(response => response.json())
    .then(data => {
        if (button) {
            if (data.success) {
                button.innerHTML = '<i class="fas fa-check"></i> Ajouté !';
                button.classList.add('btn-success');
                button.classList.remove('btn-primary');

                // Reset button after 2 seconds
                setTimeout(() => {
                    button.innerHTML = '<i class="fas fa-cart-plus"></i>';
                    button.classList.remove('btn-success');
                    button.classList.add('btn-primary');
                    button.disabled = false;
                }, 2000);

                // Add cart animation
                animateCartIcon();
                showModernAlert('Produit ajouté au panier !', 'success');
                updateCartCount();
            } else {
                button.innerHTML = '<i class="fas fa-exclamation-triangle"></i> Erreur';
                button.classList.add('btn-danger');
                button.classList.remove('btn-primary');

                setTimeout(() => {
                    button.innerHTML = '<i class="fas fa-cart-plus"></i>';
                    button.classList.remove('btn-danger');
                    button.classList.add('btn-primary');
                    button.disabled = false;
                }, 2000);

                showModernAlert(data.message || 'Erreur lors de l\'ajout au panier', 'error');
            }
        } else {
            if (data.success) {
                showModernAlert('Produit ajouté au panier !', 'success');
                updateCartCount();
            } else {
                showModernAlert(data.message || 'Erreur lors de l\'ajout au panier', 'error');
            }
        }
    })
    .catch(error => {
        console.error('Error:', error);
        if (button) {
            button.innerHTML = '<i class="fas fa-cart-plus"></i>';
            button.disabled = false;
        }
        showModernAlert('Erreur lors de l\'ajout au panier', 'error');
    });
}

// Update cart quantity
function updateCartQuantity(productId, quantity) {
    fetch('/update-cart', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            product_id: productId,
            quantity: quantity
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            location.reload(); // Reload to update totals
        } else {
            showAlert(data.message || 'Erreur lors de la mise à jour', 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showAlert('Erreur lors de la mise à jour', 'error');
    });
}

// Remove from cart
function removeFromCart(productId) {
    if (confirm('Êtes-vous sûr de vouloir supprimer ce produit du panier ?')) {
        fetch('/remove-from-cart', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                product_id: productId
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                location.reload();
            } else {
                showAlert(data.message || 'Erreur lors de la suppression', 'error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showAlert('Erreur lors de la suppression', 'error');
        });
    }
}

// Update cart count in navbar
function updateCartCount() {
    fetch('/cart-count')
    .then(response => response.json())
    .then(data => {
        const cartCountElement = document.getElementById('cart-count');
        if (cartCountElement) {
            cartCountElement.textContent = data.count || 0;
        }
    })
    .catch(error => {
        console.error('Error updating cart count:', error);
    });
}

// Modern alert system with animations
function showModernAlert(message, type = 'info') {
    // Remove existing alerts
    const existingAlerts = document.querySelectorAll('.modern-alert');
    existingAlerts.forEach(alert => alert.remove());

    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type === 'error' ? 'danger' : type} alert-dismissible fade show modern-alert`;
    alertDiv.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 9999;
        min-width: 300px;
        transform: translateX(400px);
        transition: transform 0.3s ease;
        border-radius: 15px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.15);
    `;

    alertDiv.innerHTML = `
        <div class="d-flex align-items-center">
            <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-triangle' : 'info-circle'} me-2"></i>
            <span>${message}</span>
            <button type="button" class="btn-close ms-auto" onclick="this.parentElement.parentElement.remove()"></button>
        </div>
    `;

    document.body.appendChild(alertDiv);

    // Animate in
    setTimeout(() => {
        alertDiv.style.transform = 'translateX(0)';
    }, 100);

    // Auto-dismiss after 4 seconds
    setTimeout(() => {
        alertDiv.style.transform = 'translateX(400px)';
        setTimeout(() => {
            if (alertDiv.parentNode) {
                alertDiv.remove();
            }
        }, 300);
    }, 4000);
}

// Animate cart icon when item is added
function animateCartIcon() {
    const cartIcon = document.querySelector('.navbar .fa-shopping-cart');
    if (cartIcon) {
        cartIcon.style.animation = 'pulse 0.6s ease';
        setTimeout(() => {
            cartIcon.style.animation = '';
        }, 600);
    }
}

// Legacy function for compatibility
function showAlert(message, type = 'info') {
    showModernAlert(message, type);
}

// Product search functionality with modern UX
function searchProducts() {
    const searchTerm = document.getElementById('search-input').value;
    const category = document.getElementById('category-filter').value;
    const minPrice = document.getElementById('min-price').value;
    const maxPrice = document.getElementById('max-price').value;

    // Show loading state
    const searchButton = document.querySelector('button[onclick="searchProducts()"]');
    if (searchButton) {
        const originalText = searchButton.innerHTML;
        searchButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Recherche...';
        searchButton.disabled = true;

        setTimeout(() => {
            const params = new URLSearchParams();
            if (searchTerm) params.append('search', searchTerm);
            if (category) params.append('category', category);
            if (minPrice) params.append('min_price', minPrice);
            if (maxPrice) params.append('max_price', maxPrice);

            window.location.href = '/products?' + params.toString();
        }, 500);
    } else {
        const params = new URLSearchParams();
        if (searchTerm) params.append('search', searchTerm);
        if (category) params.append('category', category);
        if (minPrice) params.append('min_price', minPrice);
        if (maxPrice) params.append('max_price', maxPrice);

        window.location.href = '/products?' + params.toString();
    }
}

// Add modern loading states to forms
document.addEventListener('DOMContentLoaded', function() {
    // Add loading states to all forms
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitButton = form.querySelector('button[type="submit"]');
            if (submitButton && !submitButton.disabled) {
                const originalText = submitButton.innerHTML;
                submitButton.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Traitement...';
                submitButton.disabled = true;

                // Re-enable after 10 seconds as fallback
                setTimeout(() => {
                    submitButton.innerHTML = originalText;
                    submitButton.disabled = false;
                }, 10000);
            }
        });
    });

    // Add smooth scroll to anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Add fade-in animation to elements
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const fadeObserver = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, observerOptions);

    // Observe elements for fade-in animation
    document.querySelectorAll('.card, .feature-card, .category-card').forEach(el => {
        el.classList.add('fade-in-up');
        fadeObserver.observe(el);
    });
});
