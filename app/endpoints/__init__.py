from flask import Blueprint

N_GRAM_METRICS = Blueprint('n_gram_metrics_api', __name__)
POS = Blueprint('pos_api', __name__)
SENTENCE_TREES = Blueprint('sentence_trees_api', __name__)
STM = Blueprint('stm_api', __name__)

BLUEPRINTS = (N_GRAM_METRICS, POS, SENTENCE_TREES, STM)

from . import n_gram_metrics, pos, sentence_trees, stm
