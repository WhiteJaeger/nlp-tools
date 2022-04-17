import os
from flask import json, request, send_from_directory
from nltk import sent_tokenize
from pathlib import Path
from spacy import displacy

from NLP.constants import METRICS_MAP, METRICS_FUNCTIONS
from NLP.text_utils import prepare_str
from constants import IMAGES_DIR
from models import SPACY_MODEL
from utils import generate_salt, purge_old_files
from server import APP


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
        prepared_hypothesis = sent_tokenize(prepared_hypothesis)
        prepared_reference = sent_tokenize(prepared_reference)
        result = METRICS_FUNCTIONS[metric]([prepared_reference], prepared_hypothesis)

    output = {
        'reference': data['reference'],
        'hypothesis': data['hypothesis'],
        'metric': METRICS_MAP[metric],
        'score': round(result, 2) if result > .001 else 0
    }
    return json.dumps(output)


@APP.route('/api/sentence-trees', methods=['POST'])
def sentence_trees():
    data = request.get_json()
    sentence = data['sentence']
    spacy_doc = SPACY_MODEL(sentence)
    output_path = os.path.join(IMAGES_DIR, f'sentence_tree_{generate_salt()}.svg')
    svg_tree = displacy.render(spacy_doc, style='dep', options={'bg': '#fafafa'})
    purge_old_files(IMAGES_DIR)

    with open(output_path, 'w', encoding='utf-8') as tree_file:
        tree_file.write(svg_tree)

    output = {
        'sentence': sentence,
        'imageSource': Path(output_path).name
    }
    return json.dumps(output)


@APP.route('/images/<path:filename>', methods=['GET'])
def serve_image(filename: str):
    return send_from_directory(IMAGES_DIR, filename)


if __name__ == '__main__':
    APP.run(debug=True)
