from flask import Flask, json, request
import datetime
from constants import UPLOADS_DIR, IMAGES_DIR, METRICS_MAP
import os
import secrets


def create_app() -> Flask:
    # Create images directory
    os.makedirs(IMAGES_DIR, exist_ok=True)

    # Setup flask app
    app = Flask(__name__)
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


@APP.route('/api/time')
def time():
    return {'time': datetime.datetime.today()}


@APP.route('/api/available-metrics')
def available_gram_metrics():
    return json.dumps(METRICS_MAP)


@APP.route('/api/n-gram-metric', methods=['POST'])
def n_gram_metric():
    data = request.get_json()
    print(data)
    return json.dumps('OK')


if __name__ == '__main__':
    APP.run(debug=True)
