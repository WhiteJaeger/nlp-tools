import os
import pathlib
import spacy
from joblib import load
from nltk.translate.bleu_score import sentence_bleu
from nltk.translate.chrf_score import sentence_chrf
from nltk.translate.gleu_score import sentence_gleu
from nltk.translate.meteor_score import single_meteor_score
from nltk.translate.nist_score import sentence_nist
from rouge import Rouge

from NLP.stm_package.subtree_metric.stm import sentence_stm, sentence_stm_augmented

APP_DIR = pathlib.Path(__file__).parent.parent.resolve()
UPLOADS_DIR = pathlib.Path().joinpath(APP_DIR, 'uploads')
IMAGES_DIR = pathlib.Path().joinpath(APP_DIR, 'images')
MODELS_DIR = pathlib.Path().joinpath(APP_DIR, 'NLP', 'models')
SERVER_MODE = os.getenv('SERVER_MODE')

SPACY_MODEL: spacy.Language = spacy.load('en_core_web_md')
POS_TAGGER = load(os.path.join(MODELS_DIR, 'posTagger.joblib'))
TF_IDF_VECTORIZER = load(os.path.join(MODELS_DIR, 'TFIDFVectorizer.joblib'))

METRICS_MAP = {
    'bleu': 'BLEU',
    'gleu': 'GLEU',
    'chrf': 'Character n-gram F-score',
    'nist': 'NIST',
    'meteor': 'METEOR',
    'rouge': 'ROUGE'
}

ROUGE = Rouge()

METRICS_FUNCTIONS = {
    'bleu': sentence_bleu,
    'gleu': sentence_gleu,
    'chrf': sentence_chrf,
    'nist': sentence_nist,
    'meteor': single_meteor_score,
    'rouge': ROUGE.get_scores,
    'stm': sentence_stm,
    'stm_augmented': sentence_stm_augmented
}

CONTRACTION_MAP = {
    "ain't": "is not",
    "aren't": "are not",
    "can't": "cannot",
    "can't've": "cannot have",
    "'cause": "because",
    "could've": "could have",
    "couldn't": "could not",
    "couldn't've": "could not have",
    "didn't": "did not",
    "doesn't": "does not",
    "don't": "do not",
    "hadn't": "had not",
    "hadn't've": "had not have",
    "hasn't": "has not",
    "haven't": "have not",
    "he'd": "he would",
    "he'd've": "he would have",
    "he'll": "he will",
    "he'll've": "he he will have",
    "he's": "he is",
    "how'd": "how did",
    "how'd'y": "how do you",
    "how'll": "how will",
    "how's": "how is",
    "I'd": "I would",
    "I'd've": "I would have",
    "I'll": "I will",
    "I'll've": "I will have",
    "I'm": "I am",
    "I've": "I have",
    "i'd": "i would",
    "i'd've": "i would have",
    "i'll": "i will",
    "i'll've": "i will have",
    "i'm": "i am",
    "i've": "i have",
    "isn't": "is not",
    "it'd": "it would",
    "it'd've": "it would have",
    "it'll": "it will",
    "it'll've": "it will have",
    "it's": "it is",
    "let's": "let us",
    "ma'am": "madam",
    "mayn't": "may not",
    "might've": "might have",
    "mightn't": "might not",
    "mightn't've": "might not have",
    "must've": "must have",
    "mustn't": "must not",
    "mustn't've": "must not have",
    "needn't": "need not",
    "needn't've": "need not have",
    "o'clock": "of the clock",
    "oughtn't": "ought not",
    "oughtn't've": "ought not have",
    "shan't": "shall not",
    "sha'n't": "shall not",
    "shan't've": "shall not have",
    "she'd": "she would",
    "she'd've": "she would have",
    "she'll": "she will",
    "she'll've": "she will have",
    "she's": "she is",
    "should've": "should have",
    "shouldn't": "should not",
    "shouldn't've": "should not have",
    "so've": "so have",
    "so's": "so as",
    "that'd": "that would",
    "that'd've": "that would have",
    "that's": "that is",
    "there'd": "there would",
    "there'd've": "there would have",
    "there's": "there is",
    "they'd": "they would",
    "they'd've": "they would have",
    "they'll": "they will",
    "they'll've": "they will have",
    "they're": "they are",
    "they've": "they have",
    "to've": "to have",
    "wasn't": "was not",
    "we'd": "we would",
    "we'd've": "we would have",
    "we'll": "we will",
    "we'll've": "we will have",
    "we're": "we are",
    "we've": "we have",
    "weren't": "were not",
    "what'll": "what will",
    "what'll've": "what will have",
    "what're": "what are",
    "what's": "what is",
    "what've": "what have",
    "when's": "when is",
    "when've": "when have",
    "where'd": "where did",
    "where's": "where is",
    "where've": "where have",
    "who'll": "who will",
    "who'll've": "who will have",
    "who's": "who is",
    "who've": "who have",
    "why's": "why is",
    "why've": "why have",
    "will've": "will have",
    "won't": "will not",
    "won't've": "will not have",
    "would've": "would have",
    "wouldn't": "would not",
    "wouldn't've": "would not have",
    "y'all": "you all",
    "y'all'd": "you all would",
    "y'all'd've": "you all would have",
    "y'all're": "you all are",
    "y'all've": "you all have",
    "you'd": "you would",
    "you'd've": "you would have",
    "you'll": "you will",
    "you'll've": "you will have",
    "you're": "you are",
    "you've": "you have"
}

# Weights are from: Sobecki, P. & Karaś, D. & Śpiewak, M. (2021)
# Tags are from: https://universaldependencies.org/u/pos/ - they are used by SpaCy
POS_WEIGHTS = {
    # e.g.: big, old, incomprehensible
    'ADJ': .13,
    # e.g.: in, to, during
    'ADP': .04,
    # e.g.: up, down, then, sometime, well, exactly
    'ADV': .1,
    # e.g.: has been
    'AUX': .13,
    # e.g.: and, or, but, if, while
    'CCONJ': .06,
    'SCONJ': .06,
    # e.g.: a, an, the, this
    'DET': .01,
    # e.g.: psst, hello
    'INTJ': 0,
    # e.g.: dog, cloud
    'NOUN': .13,
    # e.g.: 0, 1, 2, 123; one, two, seven
    'NUM': .21,
    # e.g.: not, 's
    'PART': .11,
    # e.g.: I, you, he, everyone; Mary, John
    'PRON': .09,
    'PROPN': 0.09,
    # e.g.: ",", "."
    'PUNCT': 0,
    # e.g.: $, <, =, emojis
    'SYM': 0,
    # e.g.: run, eat
    'VERB': 0.13,
    # e.g.: other
    'X': 0
}
