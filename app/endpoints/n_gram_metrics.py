from flask import request, jsonify
from flask_cors import cross_origin
from nltk import sent_tokenize

from app.constants import METRICS_MAP, METRICS_FUNCTIONS
from app.endpoints import N_GRAM_METRICS
from app.text_utils import prepare_text


@N_GRAM_METRICS.route('/available-metrics')
@cross_origin()
def available_ngram_metrics():
    return jsonify(METRICS_MAP)


@N_GRAM_METRICS.route('/n-gram-metric/all', methods=['POST'])
@cross_origin()
def all_n_gram_metrics():
    data = request.get_json()
    preprocessing = data['preprocessing']
    prepared_reference = prepare_text(text=data['reference'],
                                      lowercase=preprocessing['lowercase'],
                                      contraction_expansion=preprocessing['expandContractions'],
                                      remove_spec_characters=preprocessing['removeSpecialCharacters'])
    prepared_hypothesis = prepare_text(text=data['hypothesis'],
                                       lowercase=preprocessing['lowercase'],
                                       contraction_expansion=preprocessing['expandContractions'],
                                       remove_spec_characters=preprocessing['removeSpecialCharacters'])

    scores = {}
    for metric in METRICS_MAP:
        if metric in ('rouge', 'chrf'):
            scores[METRICS_MAP[metric]] = round(
                METRICS_FUNCTIONS[metric](prepared_reference, prepared_hypothesis), 2
            )
        elif metric == 'meteor':
            tokenized_hypothesis = sent_tokenize(prepared_hypothesis)
            tokenized_reference = sent_tokenize(prepared_reference)
            scores[METRICS_MAP[metric]] = round(
                METRICS_FUNCTIONS[metric](tokenized_reference, tokenized_hypothesis), 2
            )
        else:
            tokenized_hypothesis = sent_tokenize(prepared_hypothesis)
            tokenized_reference = sent_tokenize(prepared_reference)
            scores[METRICS_MAP[metric]] = round(
                METRICS_FUNCTIONS[metric]([tokenized_reference], tokenized_hypothesis), 2
            )

    output = {
        'reference': data['reference'],
        'hypothesis': data['hypothesis'],
        'scores': scores
    }
    return jsonify(output)


@N_GRAM_METRICS.route('/n-gram-metric/<string:metric>', methods=['POST'])
@cross_origin()
def n_gram_metric(metric: str):
    data = request.get_json()
    preprocessing = data['preprocessing']

    prepared_reference = prepare_text(text=data['reference'],
                                      lowercase=preprocessing['lowercase'],
                                      contraction_expansion=preprocessing['expandContractions'],
                                      remove_spec_characters=preprocessing['removeSpecialCharacters'])
    prepared_hypothesis = prepare_text(text=data['hypothesis'],
                                       lowercase=preprocessing['lowercase'],
                                       contraction_expansion=preprocessing['expandContractions'],
                                       remove_spec_characters=preprocessing['removeSpecialCharacters'])

    if metric in ('rouge', 'meteor', 'chrf'):
        score = METRICS_FUNCTIONS[metric](prepared_reference, prepared_hypothesis)
    else:
        prepared_hypothesis = sent_tokenize(prepared_hypothesis)
        prepared_reference = sent_tokenize(prepared_reference)
        score = METRICS_FUNCTIONS[metric]([prepared_reference], prepared_hypothesis)

    output = {
        'reference': data['reference'],
        'hypothesis': data['hypothesis'],
        'metric': METRICS_MAP[metric],
        'score': round(score, 2)
    }
    return jsonify(output)
