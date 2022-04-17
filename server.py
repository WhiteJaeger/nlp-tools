import secrets

import os
from flask import Flask

from app.constants import UPLOADS_DIR, IMAGES_DIR, SERVER_MODE


def create_app() -> Flask:
    # Create images directory
    os.makedirs(IMAGES_DIR, exist_ok=True)

    # Setup flask app
    if SERVER_MODE == 'development':
        app = Flask(__name__)
    else:
        app = Flask(__name__, static_folder='client/build', static_url_path='')
    app.secret_key = os.getenv('SECRET_KEY', secrets.token_urlsafe())

    # Max of 5MB for files
    app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024
    # Allowed ext
    app.config['UPLOAD_EXTENSIONS'] = ['.txt']
    # Uploads folder
    os.makedirs(UPLOADS_DIR, exist_ok=True)
    app.config['UPLOAD_PATH'] = UPLOADS_DIR

    return app


APP = create_app()
