from flask import request, json
from flask_cors import cross_origin

from app.constants import METRICS_FUNCTIONS, SPACY_MODEL, TF_IDF_VECTORIZER, POS_WEIGHTS
from app.endpoints import STM
from app.text_utils import prepare_text


@STM.route('/stm', methods=['POST'])
@cross_origin()
def stm():
    data = request.get_json()
    preprocessing = data['preprocessing']
    depth = int(data['depth'])

    prepared_reference = prepare_text(text=data['reference'],
                                      lowercase=preprocessing['lowercase'],
                                      contraction_expansion=preprocessing['expandContractions'],
                                      remove_spec_characters=preprocessing['removeSpecialCharacters'])
    prepared_hypothesis = prepare_text(text=data['hypothesis'],
                                       lowercase=preprocessing['lowercase'],
                                       contraction_expansion=preprocessing['expandContractions'],
                                       remove_spec_characters=preprocessing['removeSpecialCharacters'])

    score = METRICS_FUNCTIONS['stm'](reference=prepared_reference,
                                     hypothesis=prepared_hypothesis,
                                     nlp_model=SPACY_MODEL,
                                     depth=depth)

    score_augmented = METRICS_FUNCTIONS['stm_augmented'](reference=prepared_reference,
                                                         hypothesis=prepared_hypothesis,
                                                         nlp_model=SPACY_MODEL,
                                                         depth=depth,
                                                         vectorizer=TF_IDF_VECTORIZER,
                                                         pos_weights=POS_WEIGHTS)

    output = {
        'reference': data['reference'],
        'hypothesis': data['hypothesis'],
        'score': round(score, 2) if score > .001 else 0,
        'scoreAugmented': round(score_augmented, 2) if score_augmented > .001 else 0,
        'depth': depth
    }
    return json.dumps(output)
