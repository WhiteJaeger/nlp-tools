from flask import json, request
from flask_cors import cross_origin
from nltk import sent_tokenize

from app.constants import METRICS_MAP, METRICS_FUNCTIONS
from app.endpoints import N_GRAM_METRICS
from app.text_utils import prepare_text


@N_GRAM_METRICS.route('/available-metrics')
@cross_origin()
def available_gram_metrics():
    return json.dumps(METRICS_MAP)


# TODO: propagate the metric through URL
@N_GRAM_METRICS.route('/n-gram-metric', methods=['POST'])
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
        score = METRICS_FUNCTIONS[metric](prepared_reference, prepared_hypothesis)
    else:
        prepared_hypothesis = sent_tokenize(prepared_hypothesis)
        prepared_reference = sent_tokenize(prepared_reference)
        score = METRICS_FUNCTIONS[metric]([prepared_reference], prepared_hypothesis)

    output = {
        'reference': data['reference'],
        'hypothesis': data['hypothesis'],
        'metric': METRICS_MAP[metric],
        'score': round(score, 2) if score > .001 else 0
    }
    return json.dumps(output)
