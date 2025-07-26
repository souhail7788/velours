#!/usr/bin/env python3
"""
Point d'entrée WSGI pour Railway
"""

import os
from app import app

# Configuration pour Railway
if os.environ.get('RAILWAY_ENVIRONMENT'):
    app.config['DEBUG'] = False
    
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=app.config.get('DEBUG', False))
