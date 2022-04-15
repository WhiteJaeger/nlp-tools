import secrets

import datetime
import os
from flask import Flask, json, request

from NLP.constants import METRICS_MAP, METRICS_FUNCTIONS
from NLP.text_utils import prepare_str
from constants import UPLOADS_DIR, IMAGES_DIR


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
    preprocessing = data['preprocessing']
    metric = data['metric']

    prepared_reference = prepare_str(text=data['reference'],
                                     text_lower_case=preprocessing['lowercase'],
                                     contraction_expansion=preprocessing['expandContractions'],
                                     special_char_removal=preprocessing['removeSpecialCharacters'])
    prepared_hypothesis = prepare_str(text=data['hypothesis'],
                                      text_lower_case=preprocessing['lowercase'],
                                      contraction_expansion=preprocessing['expandContractions'],
                                      special_char_removal=preprocessing['removeSpecialCharacters'])

    if metric in ('rouge', 'meteor', 'chrf'):
        result = METRICS_FUNCTIONS[metric](prepared_reference, prepared_hypothesis)
    else:
        prepared_hypothesis = prepared_hypothesis.split()
        prepared_reference = prepared_reference.split()
        result = METRICS_FUNCTIONS[metric]([prepared_reference], prepared_hypothesis)

    output = {
        'reference': data['reference'],
        'hypothesis': data['hypothesis'],
        'metric': METRICS_MAP[metric],
        'score': round(result, 2) if result > .001 else 0
    }
    return json.dumps(output)


if __name__ == '__main__':
    APP.run(debug=True)
