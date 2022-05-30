import os
import pathlib
import spacy
from joblib import load
from nltk.translate.bleu_score import corpus_bleu
from nltk.translate.meteor_score import meteor_score
from nltk.translate.nist_score import corpus_nist
from typing import List
import numpy

from NLP.stm_package.subtree_metric.stm import corpus_stm, corpus_stm_augmented

numpy.seterr('raise')

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


def calculate_corpus_meteor(references_corpora: List[List[List[str]]], hypotheses: List[List[str]]) -> float:
    score = 0
    for reference, hypothesis in zip(references_corpora, hypotheses):
        score += meteor_score(reference, hypothesis)
    return score / len(references_corpora)


if __name__ == '__main__':
    APP_DIR = pathlib.Path(__file__).parent.parent.resolve()
    MODELS_DIR = pathlib.Path().joinpath(APP_DIR, 'NLP', 'models')

    SPACY_MODEL: spacy.Language = spacy.load('en_core_web_md')
    TF_IDF_VECTORIZER = load(os.path.join(MODELS_DIR, 'TFIDFVectorizer.joblib'))

    # Read corpora
    DATA_DIR = pathlib.Path(__file__).parent.resolve().joinpath('data')
    with open(DATA_DIR.joinpath('Translator1.txt'), 'r', encoding='utf-8') as f:
        reference_corpora_1 = f.read().split('\n')
        while '' in reference_corpora_1:
            reference_corpora_1.remove('')

    with open(DATA_DIR.joinpath('Translator2.txt'), 'r', encoding='utf-8') as f:
        reference_corpora_2 = f.read().split('\n')
        while '' in reference_corpora_2:
            reference_corpora_2.remove('')

    with open(DATA_DIR.joinpath('Translator3.txt'), 'r', encoding='utf-8') as f:
        reference_corpora_3 = f.read().split('\n')
        while '' in reference_corpora_3:
            reference_corpora_3.remove('')

    with open(DATA_DIR.joinpath('Translator4.txt'), 'r', encoding='utf-8') as f:
        reference_corpora_4 = f.read().split('\n')
        while '' in reference_corpora_4:
            reference_corpora_4.remove('')

    # Transform corpora
    ## N-gram metrics digestible
    reference_corpora_1_for_ngram = [[sentence.split()] for sentence in reference_corpora_1][:500]
    hypothesis_corpora_1_for_ngram = [sentence.split() for sentence in reference_corpora_1][:500]

    reference_corpora_2_for_ngram = [[sentence.split()] for sentence in reference_corpora_2][:500]
    hypothesis_corpora_2_for_ngram = [sentence.split() for sentence in reference_corpora_2][:500]

    reference_corpora_3_for_ngram = [[sentence.split()] for sentence in reference_corpora_3][:500]
    hypothesis_corpora_3_for_ngram = [sentence.split() for sentence in reference_corpora_3][:500]

    reference_corpora_4_for_ngram = [[sentence.split()] for sentence in reference_corpora_4][:500]
    hypothesis_corpora_4_for_ngram = [sentence.split() for sentence in reference_corpora_4][:500]

    ## stm_package digestible
    reference_corpora_1_for_stm = reference_corpora_1[:500]
    reference_corpora_2_for_stm = reference_corpora_2[:500]
    reference_corpora_3_for_stm = reference_corpora_3[:500]
    reference_corpora_4_for_stm = reference_corpora_4[:500]

    # Evaluation
    print('FIRST vs. FIRST')  # Sanity check that evaluation is done right and metrics are close to 1
    print(f'BLEU: {corpus_bleu(reference_corpora_1_for_ngram, hypothesis_corpora_1_for_ngram)}')
    print(f'NIST: {corpus_nist(reference_corpora_1_for_ngram, hypothesis_corpora_1_for_ngram)}')
    print(f'METEOR: {calculate_corpus_meteor(reference_corpora_1_for_ngram, hypothesis_corpora_1_for_ngram)}')
    print(f'STM: {corpus_stm(reference_corpora_1_for_stm, reference_corpora_1_for_stm, SPACY_MODEL, 3)}')
    print(
        f'STM-A: {corpus_stm_augmented(reference_corpora_1_for_stm, reference_corpora_1_for_stm, SPACY_MODEL, 3, TF_IDF_VECTORIZER, POS_WEIGHTS)}')

    print('*' * 100)
    print('SECOND vs. SECOND')  # Sanity check that evaluation is done right and metrics are close to 1
    print(f'BLEU: {corpus_bleu(reference_corpora_2_for_ngram, hypothesis_corpora_2_for_ngram)}')
    print(f'NIST: {corpus_nist(reference_corpora_2_for_ngram, hypothesis_corpora_2_for_ngram)}')
    print(f'METEOR: {calculate_corpus_meteor(reference_corpora_2_for_ngram, hypothesis_corpora_2_for_ngram)}')
    print(f'STM: {corpus_stm(reference_corpora_2_for_stm, reference_corpora_2_for_stm, SPACY_MODEL, 3)}')
    print(
        f'STM-A: {corpus_stm_augmented(reference_corpora_2_for_stm, reference_corpora_2_for_stm, SPACY_MODEL, 3, TF_IDF_VECTORIZER, POS_WEIGHTS)}')

    print('*' * 100)
    print('THIRD vs. THIRD')  # Sanity check that evaluation is done right and metrics are close to 1
    print(f'BLEU: {corpus_bleu(reference_corpora_3_for_ngram, hypothesis_corpora_3_for_ngram)}')
    print(f'NIST: {corpus_nist(reference_corpora_3_for_ngram, hypothesis_corpora_3_for_ngram)}')
    print(f'METEOR: {calculate_corpus_meteor(reference_corpora_3_for_ngram, hypothesis_corpora_3_for_ngram)}')
    print(f'STM: {corpus_stm(reference_corpora_3_for_stm, reference_corpora_3_for_stm, SPACY_MODEL, 3)}')
    print(
        f'STM-A: {corpus_stm_augmented(reference_corpora_3_for_stm, reference_corpora_3_for_stm, SPACY_MODEL, 3, TF_IDF_VECTORIZER, POS_WEIGHTS)}')

    print('*' * 100)
    print('FOURTH vs. FOURTH')  # Sanity check that evaluation is done right and metrics are close to 1
    print(f'BLEU: {corpus_bleu(reference_corpora_4_for_ngram, hypothesis_corpora_4_for_ngram)}')
    print(f'NIST: {corpus_nist(reference_corpora_4_for_ngram, hypothesis_corpora_4_for_ngram)}')
    print(f'METEOR: {calculate_corpus_meteor(reference_corpora_4_for_ngram, hypothesis_corpora_4_for_ngram)}')
    print(f'STM: {corpus_stm(reference_corpora_4_for_stm, reference_corpora_4_for_stm, SPACY_MODEL, 3)}')
    print(
        f'STM-A: {corpus_stm_augmented(reference_corpora_4_for_stm, reference_corpora_4_for_stm, SPACY_MODEL, 3, TF_IDF_VECTORIZER, POS_WEIGHTS)}')

    print('*' * 100)
    print('FIRST vs. SECOND')
    print(f'BLEU: {corpus_bleu(reference_corpora_1_for_ngram, hypothesis_corpora_2_for_ngram)}')
    print(f'NIST: {corpus_nist(reference_corpora_1_for_ngram, hypothesis_corpora_2_for_ngram)}')
    print(f'METEOR: {calculate_corpus_meteor(reference_corpora_1_for_ngram, hypothesis_corpora_2_for_ngram)}')
    print(f'STM: {corpus_stm(reference_corpora_1_for_stm, reference_corpora_2_for_stm, SPACY_MODEL, 3)}')
    print(
        f'STM-A: {corpus_stm_augmented(reference_corpora_1_for_stm, reference_corpora_2_for_stm, SPACY_MODEL, 3, TF_IDF_VECTORIZER, POS_WEIGHTS)}')

    print('*' * 100)
    print('FIRST vs. THIRD')
    print(f'BLEU: {corpus_bleu(reference_corpora_1_for_ngram, hypothesis_corpora_3_for_ngram)}')
    print(f'NIST: {corpus_nist(reference_corpora_1_for_ngram, hypothesis_corpora_3_for_ngram)}')
    print(f'METEOR: {calculate_corpus_meteor(reference_corpora_1_for_ngram, hypothesis_corpora_3_for_ngram)}')
    print(f'STM: {corpus_stm(reference_corpora_1_for_stm, reference_corpora_3_for_stm, SPACY_MODEL, 3)}')
    print(
        f'STM-A: {corpus_stm_augmented(reference_corpora_1_for_stm, reference_corpora_3_for_stm, SPACY_MODEL, 3, TF_IDF_VECTORIZER, POS_WEIGHTS)}')

    print('*' * 100)
    print('FIRST vs. FOURTH')
    print(f'BLEU: {corpus_bleu(reference_corpora_1_for_ngram, hypothesis_corpora_4_for_ngram)}')
    print(f'NIST: {corpus_nist(reference_corpora_1_for_ngram, hypothesis_corpora_4_for_ngram)}')
    print(f'METEOR: {calculate_corpus_meteor(reference_corpora_1_for_ngram, hypothesis_corpora_4_for_ngram)}')
    print(f'STM: {corpus_stm(reference_corpora_1_for_stm, reference_corpora_4_for_stm, SPACY_MODEL, 3)}')
    print(
        f'STM-A: {corpus_stm_augmented(reference_corpora_1_for_stm, reference_corpora_4_for_stm, SPACY_MODEL, 3, TF_IDF_VECTORIZER, POS_WEIGHTS)}')

    print('*' * 100)
    print('SECOND vs. THIRD')
    print(f'BLEU: {corpus_bleu(reference_corpora_2_for_ngram, hypothesis_corpora_3_for_ngram)}')
    print(f'NIST: {corpus_nist(reference_corpora_2_for_ngram, hypothesis_corpora_3_for_ngram)}')
    print(f'METEOR: {calculate_corpus_meteor(reference_corpora_2_for_ngram, hypothesis_corpora_3_for_ngram)}')
    print(f'STM: {corpus_stm(reference_corpora_2_for_stm, reference_corpora_3_for_stm, SPACY_MODEL, 3)}')
    print(
        f'STM-A: {corpus_stm_augmented(reference_corpora_2_for_stm, reference_corpora_3_for_stm, SPACY_MODEL, 3, TF_IDF_VECTORIZER, POS_WEIGHTS)}')

    print('*' * 100)
    print('SECOND vs. FOURTH')
    print(f'BLEU: {corpus_bleu(reference_corpora_2_for_ngram, hypothesis_corpora_4_for_ngram)}')
    print(f'NIST: {corpus_nist(reference_corpora_2_for_ngram, hypothesis_corpora_4_for_ngram)}')
    print(f'METEOR: {calculate_corpus_meteor(reference_corpora_2_for_ngram, hypothesis_corpora_4_for_ngram)}')
    print(f'STM: {corpus_stm(reference_corpora_2_for_stm, reference_corpora_4_for_stm, SPACY_MODEL, 3)}')
    print(
        f'STM-A: {corpus_stm_augmented(reference_corpora_2_for_stm, reference_corpora_4_for_stm, SPACY_MODEL, 3, TF_IDF_VECTORIZER, POS_WEIGHTS)}')

    print('*' * 100)
    print('THIRD vs. FOURTH')
    print(f'BLEU: {corpus_bleu(reference_corpora_3_for_ngram, hypothesis_corpora_4_for_ngram)}')
    print(f'NIST: {corpus_nist(reference_corpora_3_for_ngram, hypothesis_corpora_4_for_ngram)}')
    print(f'METEOR: {calculate_corpus_meteor(reference_corpora_3_for_ngram, hypothesis_corpora_4_for_ngram)}')
    print(f'STM: {corpus_stm(reference_corpora_3_for_stm, reference_corpora_4_for_stm, SPACY_MODEL, 3)}')
    print(
        f'STM-A: {corpus_stm_augmented(reference_corpora_3_for_stm, reference_corpora_4_for_stm, SPACY_MODEL, 3, TF_IDF_VECTORIZER, POS_WEIGHTS)}')

    print('*' * 100)
    print('THIRD vs. FOURTH')
    print(f'STM 1-length trees: {corpus_stm(reference_corpora_3_for_stm, reference_corpora_4_for_stm, SPACY_MODEL, 1)}')
    print(
        f'STM-A 1-length trees: {corpus_stm_augmented(reference_corpora_3_for_stm, reference_corpora_4_for_stm, SPACY_MODEL, 1, TF_IDF_VECTORIZER, POS_WEIGHTS)}')

    print(f'STM 2-length trees: {corpus_stm(reference_corpora_3_for_stm, reference_corpora_4_for_stm, SPACY_MODEL, 2)}')
    print(
        f'STM-A 2-length trees: {corpus_stm_augmented(reference_corpora_3_for_stm, reference_corpora_4_for_stm, SPACY_MODEL, 2, TF_IDF_VECTORIZER, POS_WEIGHTS)}')


# Results
# FIRST vs. FIRST
# BLEU: 0.9982658457109393
# NIST: 13.368063436646528
# METEOR: 0.990656415293831
# STM: 0.9767
# STM-A: 0.9759
# ****************************************************************************************************
# SECOND vs. SECOND
# BLEU: 0.9985326056013665
# NIST: 13.40738431626326
# METEOR: 0.9917533267389756
# STM: 0.9787
# STM-A: 0.978
# ****************************************************************************************************
# THIRD vs. THIRD
# BLEU: 0.998600666554106
# NIST: 13.459377684123789
# METEOR: 0.9900119195141466
# STM: 0.9773
# STM-A: 0.977
# ****************************************************************************************************
# FOURTH vs. FOURTH
# BLEU: 0.9982619856334487
# NIST: 13.36410770854072
# METEOR: 0.9914935222967163
# STM: 0.978
# STM-A: 0.9775
# ****************************************************************************************************
# FIRST vs. SECOND
# BLEU: 0.3131650301477595
# NIST: 6.842192206781902
# METEOR: 0.6051512192141372
# STM: 0.5415
# STM-A: 0.5079
# ****************************************************************************************************
# FIRST vs. THIRD
# BLEU: 0.24805461218182004
# NIST: 5.8718347913668145
# METEOR: 0.5434937700643819
# STM: 0.4928
# STM-A: 0.4543
# ****************************************************************************************************
# FIRST vs. FOURTH
# BLEU: 0.5076389102316189
# NIST: 9.22117726382084
# METEOR: 0.7739095872876394
# STM: 0.682
# STM-A: 0.6556
# ****************************************************************************************************
# SECOND vs. THIRD
# BLEU: 0.23689570084576927
# NIST: 5.694706837152382
# METEOR: 0.5202702108428783
# STM: 0.4972
# STM-A: 0.4592
# ****************************************************************************************************
# SECOND vs. FOURTH
# BLEU: 0.37067794028495965
# NIST: 7.656434932184833
# METEOR: 0.6406266536661465
# STM: 0.5804
# STM-A: 0.548
# ****************************************************************************************************
# THIRD vs. FOURTH
# BLEU: 0.2665348537463917
# NIST: 6.439588648675369
# METEOR: 0.5443216777265093
# STM: 0.5321
# STM-A: 0.4929
# ****************************************************************************************************
# THIRD vs. FOURTH
# STM 1-length trees: 0.9354
# STM-A 1-length trees: 0.9354
# STM 2-length trees: 0.6942
# STM-A 2-length trees: 0.6444
