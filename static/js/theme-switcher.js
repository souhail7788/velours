// 🎨 Système de changement de thème pour Velours Parfum

class ThemeSwitcher {
    constructor() {
        this.themes = {
            luxury: {
                name: 'Luxe Moderne',
                colors: {
                    primary: '#1a1a2e',
                    secondary: '#16213e',
                    accent: '#e94560',
                    gold: '#f39c12'
                }
            },
            gold: {
                name: 'Élégance Dorée',
                colors: {
                    primary: '#2c1810',
                    secondary: '#3d2817',
                    accent: '#d4af37',
                    gold: '#ffd700'
                }
            },
            rose: {
                name: 'Minimalisme Rose',
                colors: {
                    primary: '#2d3436',
                    secondary: '#636e72',
                    accent: '#fd79a8',
                    gold: '#e84393'
                }
            },
            nature: {
                name: 'Nature Verte',
                colors: {
                    primary: '#2d3436',
                    secondary: '#636e72',
                    accent: '#00b894',
                    gold: '#00cec9'
                }
            },
            purple: {
                name: 'Sombre Violet',
                colors: {
                    primary: '#2d1b69',
                    secondary: '#3742fa',
                    accent: '#a55eea',
                    gold: '#8c7ae6'
                }
            }
        };
        
        this.currentTheme = localStorage.getItem('velours-parfum-theme') || 'luxury';
        this.init();
    }
    
    init() {
        this.createThemeSelector();
        this.applyTheme(this.currentTheme);
        this.bindEvents();
    }
    
    createThemeSelector() {
        const selector = document.createElement('div');
        selector.className = 'theme-selector';
        selector.innerHTML = `
            <div class="theme-selector-header mb-3">
                <h6 class="mb-0">🎨 Thèmes</h6>
                <button class="btn-close btn-close-theme" onclick="this.parentElement.parentElement.classList.remove('active')"></button>
            </div>
            <div class="theme-options">
                ${Object.keys(this.themes).map(key => `
                    <div class="theme-option ${key}" 
                         data-theme="${key}" 
                         title="${this.themes[key].name}"
                         onclick="themeSwitcher.switchTheme('${key}')">
                    </div>
                `).join('')}
            </div>
            <div class="mt-3">
                <button class="btn btn-sm btn-outline-secondary w-100" onclick="themeSwitcher.toggleDarkMode()">
                    <i class="fas fa-moon"></i> Mode sombre
                </button>
            </div>
        `;
        
        document.body.appendChild(selector);
        
        // Bouton pour ouvrir le sélecteur
        const toggleButton = document.createElement('button');
        toggleButton.className = 'btn btn-primary theme-toggle-btn';
        toggleButton.innerHTML = '<i class="fas fa-palette"></i>';
        toggleButton.style.cssText = `
            position: fixed;
            bottom: 20px;
            right: 20px;
            z-index: 999;
            border-radius: 50%;
            width: 60px;
            height: 60px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        `;
        toggleButton.onclick = () => selector.classList.toggle('active');
        
        document.body.appendChild(toggleButton);
    }
    
    switchTheme(themeName) {
        if (this.themes[themeName]) {
            this.currentTheme = themeName;
            this.applyTheme(themeName);
            localStorage.setItem('velours-parfum-theme', themeName);
            
            // Feedback visuel
            this.showThemeNotification(`Thème "${this.themes[themeName].name}" appliqué !`);
        }
    }
    
    applyTheme(themeName) {
        const theme = this.themes[themeName];
        if (!theme) return;
        
        const root = document.documentElement;
        
        // Appliquer les couleurs du thème
        root.style.setProperty('--primary-color', theme.colors.primary);
        root.style.setProperty('--secondary-color', theme.colors.secondary);
        root.style.setProperty('--accent-color', theme.colors.accent);
        root.style.setProperty('--gold-accent', theme.colors.gold);
        
        // Mettre à jour les dégradés
        const gradientLuxury = `linear-gradient(135deg, ${theme.colors.primary} 0%, ${theme.colors.secondary} 50%, ${theme.colors.accent} 100%)`;
        const gradientAccent = `linear-gradient(135deg, ${theme.colors.accent} 0%, ${theme.colors.gold} 100%)`;
        
        root.style.setProperty('--gradient-luxury', gradientLuxury);
        root.style.setProperty('--gradient-accent', gradientAccent);
        
        // Marquer le thème actif
        document.querySelectorAll('.theme-option').forEach(option => {
            option.classList.toggle('active', option.dataset.theme === themeName);
        });
        
        // Ajouter une classe au body pour les styles spécifiques
        document.body.className = document.body.className.replace(/theme-\w+/g, '');
        document.body.classList.add(`theme-${themeName}`);
    }
    
    toggleDarkMode() {
        document.body.classList.toggle('dark-mode');
        const isDark = document.body.classList.contains('dark-mode');
        localStorage.setItem('velours-parfum-dark-mode', isDark);
        
        this.showThemeNotification(isDark ? 'Mode sombre activé' : 'Mode clair activé');
    }
    
    showThemeNotification(message) {
        // Supprimer les notifications existantes
        const existing = document.querySelector('.theme-notification');
        if (existing) existing.remove();
        
        const notification = document.createElement('div');
        notification.className = 'theme-notification';
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            left: 50%;
            transform: translateX(-50%);
            background: var(--gradient-accent);
            color: white;
            padding: 12px 24px;
            border-radius: 25px;
            font-weight: 600;
            z-index: 10000;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            animation: slideInDown 0.3s ease;
        `;
        notification.textContent = message;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.style.animation = 'slideOutUp 0.3s ease';
            setTimeout(() => notification.remove(), 300);
        }, 2000);
    }
    
    bindEvents() {
        // Restaurer le mode sombre si activé
        if (localStorage.getItem('velours-parfum-dark-mode') === 'true') {
            document.body.classList.add('dark-mode');
        }
        
        // Raccourcis clavier
        document.addEventListener('keydown', (e) => {
            if (e.ctrlKey && e.shiftKey) {
                switch(e.key) {
                    case 'T':
                        e.preventDefault();
                        document.querySelector('.theme-selector').classList.toggle('active');
                        break;
                    case 'D':
                        e.preventDefault();
                        this.toggleDarkMode();
                        break;
                }
            }
        });
    }
}

// Animations CSS pour les notifications
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInDown {
        from { transform: translateX(-50%) translateY(-100%); opacity: 0; }
        to { transform: translateX(-50%) translateY(0); opacity: 1; }
    }
    
    @keyframes slideOutUp {
        from { transform: translateX(-50%) translateY(0); opacity: 1; }
        to { transform: translateX(-50%) translateY(-100%); opacity: 0; }
    }
    
    .theme-selector {
        position: fixed;
        top: 50%;
        right: 20px;
        transform: translateY(-50%);
        z-index: 1000;
        background: white;
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        min-width: 200px;
        display: none;
        backdrop-filter: blur(10px);
    }
    
    .theme-selector.active {
        display: block;
        animation: fadeInScale 0.3s ease;
    }
    
    @keyframes fadeInScale {
        from { opacity: 0; transform: translateY(-50%) scale(0.9); }
        to { opacity: 1; transform: translateY(-50%) scale(1); }
    }
    
    .theme-selector-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid #eee;
        padding-bottom: 10px;
    }
    
    .theme-option {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        margin: 8px 5px;
        cursor: pointer;
        border: 3px solid transparent;
        transition: all 0.3s ease;
        display: inline-block;
        position: relative;
    }
    
    .theme-option:hover {
        transform: scale(1.1);
        border-color: var(--accent-color);
    }
    
    .theme-option.active {
        border-color: var(--accent-color);
        box-shadow: 0 0 0 2px rgba(233, 69, 96, 0.3);
    }
    
    .theme-option.luxury { background: linear-gradient(135deg, #1a1a2e, #e94560); }
    .theme-option.gold { background: linear-gradient(135deg, #2c1810, #d4af37); }
    .theme-option.rose { background: linear-gradient(135deg, #2d3436, #fd79a8); }
    .theme-option.nature { background: linear-gradient(135deg, #2d3436, #00b894); }
    .theme-option.purple { background: linear-gradient(135deg, #2d1b69, #a55eea); }
    
    .theme-toggle-btn {
        transition: all 0.3s ease;
    }
    
    .theme-toggle-btn:hover {
        transform: scale(1.1);
    }
`;
document.head.appendChild(style);

// Initialiser le système de thèmes
let themeSwitcher;
document.addEventListener('DOMContentLoaded', () => {
    themeSwitcher = new ThemeSwitcher();
});
