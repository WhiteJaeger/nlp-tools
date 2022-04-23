import os
from flask import request, json, send_from_directory
from flask_cors import cross_origin
from pathlib import Path
from spacy import displacy

from app.constants import SPACY_MODEL, IMAGES_DIR
from app.endpoints import SENTENCE_TREES
from app.utils import purge_old_files, generate_salt


@SENTENCE_TREES.route('/sentence-trees', methods=['POST'])
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


@SENTENCE_TREES.route('/images/<path:filename>', methods=['GET'])
@cross_origin()
def serve_image(filename: str):
    return send_from_directory(IMAGES_DIR, filename)
