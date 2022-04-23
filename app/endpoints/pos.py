from flask import json, request
from flask_cors import cross_origin

from app.constants import POS_TAGGER
from app.endpoints import POS
from app.text_utils import prepare_sentence_for_pos_tagging, map_word_to_pos


@POS.route('/pos', methods=['POST'])
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
