import numpy
from numpy import dot
from numpy.linalg import norm
from sklearn.feature_extraction.text import TfidfVectorizer
from spacy.tokens import Doc


def cosine_similarity(vector_1: numpy.ndarray, vector_2: numpy.ndarray) -> float:
    if not vector_1.any() or not vector_2.any():
        return 0
    return dot(vector_1, vector_2) / (norm(vector_1) * norm(vector_2))


def get_elementwise_vectors_sum(vectors: numpy.ndarray) -> numpy.ndarray:
    return numpy.sum([*vectors], axis=0)


def get_tfidf_scores_for_words(text: str, vectorizer: TfidfVectorizer) -> dict:
    feature_names = vectorizer.get_feature_names_out()
    tfidf_matrix = vectorizer.transform([text]).todense()
    feature_index = tfidf_matrix[0, :].nonzero()[1]
    tfidf_scores = zip([feature_names[i] for i in feature_index], [tfidf_matrix[0, x] for x in feature_index])
    return dict(tfidf_scores)


def apply_pos_and_tfidf_weights_to_doc_vectors(doc: Doc,
                                               pos_weights: dict) -> numpy.ndarray:
    weighted_vectors = []
    for token in doc:
        if token.pos_ not in pos_weights or not token.vector.any():
            continue
        weighted_vectors.append(token.vector * pos_weights[token.pos_])
    return numpy.array(weighted_vectors)


def get_similarity_between_docs(first_doc: Doc,
                                second_doc: Doc,
                                pos_weights: dict) -> float:
    weighted_vectors_first_doc = apply_pos_and_tfidf_weights_to_doc_vectors(first_doc,
                                                                            pos_weights)
    weighted_vectors_second_doc = apply_pos_and_tfidf_weights_to_doc_vectors(second_doc,
                                                                             pos_weights)

    vector_first_doc = get_elementwise_vectors_sum(weighted_vectors_first_doc)
    vector_second_doc = get_elementwise_vectors_sum(weighted_vectors_second_doc)

    return cosine_similarity(vector_first_doc, vector_second_doc)
