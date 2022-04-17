import os
import pathlib
import spacy
from joblib import load

APP_DIR = pathlib.Path(__file__).parent.parent.resolve()
UPLOADS_DIR = pathlib.Path().joinpath(APP_DIR, 'uploads')
IMAGES_DIR = pathlib.Path().joinpath(APP_DIR, 'images')
MODELS_DIR = pathlib.Path().joinpath(APP_DIR, 'models')
SERVER_MODE = os.getenv('SERVER_MODE')

SPACY_MODEL: spacy.Language = spacy.load('en_core_web_md')
POS_TAGGER = load(os.path.join(MODELS_DIR, 'posTagger.joblib'))
