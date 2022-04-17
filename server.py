import secrets

import os
from flask import Flask, send_from_directory
from flask_cors import CORS

from app.constants import UPLOADS_DIR, IMAGES_DIR, SERVER_MODE
from app import api


def create_app() -> Flask:
    # Create images directory
    os.makedirs(IMAGES_DIR, exist_ok=True)

    # Setup flask app
    if SERVER_MODE == 'development':
        app = Flask(__name__)
    else:
        app = Flask(__name__, static_folder='client/build', static_url_path='')
        cors = CORS(app)
    app.secret_key = os.getenv('SECRET_KEY', secrets.token_urlsafe())

    # Max of 5MB for files
    app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024
    # Allowed ext
    app.config['UPLOAD_EXTENSIONS'] = ['.txt']
    # Uploads folder
    os.makedirs(UPLOADS_DIR, exist_ok=True)
    app.config['UPLOAD_PATH'] = UPLOADS_DIR
    app.register_blueprint(api.api_bp)

    return app


APP = create_app()


@APP.route('/')
def serve():
    return send_from_directory(APP.static_folder, 'index.html')


if __name__ == '__main__':
    APP.run(debug=True)
