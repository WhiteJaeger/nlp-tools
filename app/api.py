import os
from flask import json, request, send_from_directory, Blueprint
from flask_cors import cross_origin
from nltk import sent_tokenize
from pathlib import Path
from spacy import displacy

from constants import IMAGES_DIR, SPACY_MODEL, POS_TAGGER, METRICS_MAP, METRICS_FUNCTIONS
from text_utils import prepare_text, prepare_sentence_for_pos_tagging, map_word_to_pos
from utils import generate_salt, purge_old_files

api_bp = Blueprint('api', __name__, url_prefix='/api')


@api_bp.route('/available-metrics')
@cross_origin()
def available_gram_metrics():
    return json.dumps(METRICS_MAP)


@api_bp.route('/n-gram-metric', methods=['POST'])
@cross_origin()
def n_gram_metric():
    data = request.get_json()
    preprocessing = data['preprocessing']
    metric = data['metric']

    prepared_reference = prepare_text(text=data['reference'],
                                      lowercase=preprocessing['lowercase'],
                                      contraction_expansion=preprocessing['expandContractions'],
                                      remove_spec_characters=preprocessing['removeSpecialCharacters'])
    prepared_hypothesis = prepare_text(text=data['hypothesis'],
                                       lowercase=preprocessing['lowercase'],
                                       contraction_expansion=preprocessing['expandContractions'],
                                       remove_spec_characters=preprocessing['removeSpecialCharacters'])

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


@api_bp.route('/sentence-trees', methods=['POST'])
@cross_origin()
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


@api_bp.route('/pos', methods=['POST'])
@cross_origin()
def pos():
    data = request.get_json()
    sentence = data['sentence']
    result = prepare_sentence_for_pos_tagging(sentence)
    predicted_pos = POS_TAGGER.predict(result['pos_tagging_ready_sentence'])[0]
    output = {
        'sentence': sentence,
        'posTags': map_word_to_pos(result['cleared_sentence'], predicted_pos)
    }
    return json.dumps(output)


@api_bp.route('/images/<path:filename>', methods=['GET'])
@cross_origin()
def serve_image(filename: str):
    return send_from_directory(IMAGES_DIR, filename)
