"""
Subtree evaluation metric as described in 'Syntactic Features for Evaluation of Machine Translation' by
Ding Liu and Daniel Gildea, 2005, Association for Computational Linguistics, Pages: 25–32
@inproceedings{liu-gildea-2005-syntactic,
    title = "Syntactic Features for Evaluation of Machine Translation",
    author = "Liu, Ding  and
      Gildea, Daniel",
    booktitle = "Proceedings of the {ACL} Workshop on Intrinsic and Extrinsic Evaluation Measures for Machine
    Translation and/or Summarization",
    month = jun,
    year = "2005",
    address = "Ann Arbor, Michigan",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/W05-0904",
    pages = "25--32",
}
"""

import spacy
from spacy import Language
from spacy.tokens import Token
from subtree_metric.tree_constructor import SyntaxTreeHeadsExtractor, SyntaxTreeElementsExtractor
from typing import Union, Tuple, List, Dict


def transform_into_tags(tokens: Tuple[Token]) -> tuple:
    """
    Return a tag collection for the given tokens.
    :param tokens: tokens for which to get tags
    :type tokens: tuple[Token]
    :return: a collection of tags
    :rtype: tuple
    """
    # TODO: align some tags: e.g. VBZ - VB
    return tuple([token.tag_ for token in tokens])


def get_freq_dict_for_tags(tags: tuple) -> dict:
    """
    Construct a frequency dictionary for the given tags
    :param tags:
    :type tags: tuple
    :return: a frequency dictionary
    :rtype: dict
    """
    result = {}
    for tag in tags:
        result[tag] = result.get(tag, 0) + 1
    return result


def are_descendants_identical(ref_extractor: SyntaxTreeElementsExtractor,
                              hyp_extractor: SyntaxTreeElementsExtractor) -> bool:
    """
    Check whether children of the given heads are identical
    :param ref_extractor: already filled in extractor (containing head -> children) for the reference
    :type ref_extractor: SyntaxTreeElementsExtractor
    :param hyp_extractor: already filled in extractor (containing head -> children) for the hypothesis
    :type hyp_extractor: SyntaxTreeElementsExtractor
    :return: whether children of these heads are identical
    :rtype: bool
    """
    ref_children_tags = transform_into_tags(ref_extractor.children)
    hyp_children_tags = transform_into_tags(hyp_extractor.children)

    ref_grandchildren_tags = transform_into_tags(ref_extractor.grand_children)
    hyp_grandchildren_tags = transform_into_tags(hyp_extractor.grand_children)

    # Naive assumption - tags can be from different heads
    # TODO: compare per-head
    are_children_identical = sorted(ref_children_tags) == sorted(hyp_children_tags)
    are_grandchildren_identical = sorted(ref_grandchildren_tags) == sorted(hyp_grandchildren_tags)

    return are_children_identical and are_grandchildren_identical


def sentence_stm(reference: str, hypothesis: str, nlp_model: Language, depth: int = 3) -> float:
    """
    Calculate sentence-level Subtree Metric score.
        >>> hypothesis = 'It is a guide to action which ensures that the military always obeys the commands of the party'
        >>> reference = 'It is the guiding to action that ensures that the military will forever heed Party commands'
        >>> sentence_stm(reference, hypothesis, spacy_model, depth=3)
        0.4444
    :param reference: reference sentence
    :type reference: str
    :param hypothesis: hypothesis sentence
    :type hypothesis: str
    :param nlp_model: one of the SpaCy NLP models with support of the DependencyParser (https://spacy.io/models)
    :type nlp_model: Language
    :param depth: depth of the subtrees to take into account
    :type depth: int
    :return: stm score
    :rtype: float
    """
    score = 0.0
    # Get output from SpaCy model
    reference_preprocessed = nlp_model(reference)
    hypothesis_preprocessed = nlp_model(hypothesis)

    # Get heads of syntax trees
    sentence_tree_heads_reference = SyntaxTreeHeadsExtractor(reference_preprocessed)
    sentence_tree_heads_hypothesis = SyntaxTreeHeadsExtractor(hypothesis_preprocessed)

    tags_first_level_hyp = transform_into_tags(sentence_tree_heads_hypothesis.first_level_heads)

    # Get frequencies of individual tags
    tags_frequencies_ref = get_freq_dict_for_tags(transform_into_tags(sentence_tree_heads_reference.first_level_heads))
    tags_frequencies_hyp = get_freq_dict_for_tags(transform_into_tags(sentence_tree_heads_hypothesis.first_level_heads))

    # Compute for 1-level-trees, i.e. individual tags
    count = 0
    for tag in tags_frequencies_hyp:
        # Get already clipped value - number of times a tag appears in reference
        count += tags_frequencies_ref.get(tag, 0)
    score += count / len(tags_first_level_hyp) if len(tags_first_level_hyp) else 0

    if depth >= 2:
        # Compute for 2-level-trees
        used_heads_indexes = []
        count = 0
        for two_level_head_hyp in sentence_tree_heads_hypothesis.second_level_heads:
            for idx, two_level_head_ref in enumerate(sentence_tree_heads_reference.second_level_heads):
                if idx in used_heads_indexes:
                    continue
                if two_level_head_hyp.tag_ == two_level_head_ref.tag_:
                    # Get children
                    ref_children_tags = transform_into_tags(SyntaxTreeElementsExtractor(two_level_head_ref).children)
                    hyp_children_tags = transform_into_tags(SyntaxTreeElementsExtractor(two_level_head_hyp).children)
                    # Check if their children are identical
                    if sorted(ref_children_tags) == sorted(hyp_children_tags):
                        count += 1
                        used_heads_indexes.append(idx)
        score += count / len(sentence_tree_heads_hypothesis.second_level_heads) \
            if len(sentence_tree_heads_hypothesis.second_level_heads) else 0

    if depth >= 3:
        # Compute for 3-level-trees
        count = 0
        third_level_hyp = sentence_tree_heads_hypothesis.third_level_heads
        third_level_ref = sentence_tree_heads_reference.third_level_heads
        used_heads_indexes = []
        for third_level_head_hyp in third_level_hyp:
            # Same as in 2-level
            for idx, third_level_head_ref in enumerate(third_level_ref):
                if idx in used_heads_indexes:
                    continue
                if third_level_head_hyp.tag_ == third_level_head_ref.tag_:
                    # Get children & grandchildren
                    extractor_ref = SyntaxTreeElementsExtractor(third_level_head_ref)
                    extractor_hyp = SyntaxTreeElementsExtractor(third_level_head_hyp)
                    # Check if their children & grandchildren are identical
                    if are_descendants_identical(extractor_ref, extractor_hyp):
                        count += 1
                        used_heads_indexes.append(idx)

        score += count / len(third_level_hyp) if len(third_level_hyp) else 0

    return round(score / depth, 4)


def corpus_stm(references: List[str],
               hypotheses: List[str],
               nlp_model: Language,
               depth: int) -> float:
    """
    Calculate corpus-level Subtree Metric score
    :param hypotheses: hypotheses
    :type hypotheses: list[str]
    :param references: references
    :type references: list[str]
    :param nlp_model: one of the SpaCy NLP models with support of the DependencyParser (https://spacy.io/models)
    :type nlp_model: Language
    :param depth: depth of the subtrees to take into account
    :type depth: int
    :return: Corpus stm_package score
    :rtype: float
    """

    score = 0

    for reference_sentence, hypothesis_sentence in zip(references, hypotheses):
        score += sentence_stm(reference_sentence, hypothesis_sentence, nlp_model, depth)

    return round(score / len(references), 4)


def corpus_stm_augmented(references: List[str],
                         hypotheses: List[str],
                         nlp_model: Language,
                         depth: int = 3,
                         make_summary: bool = True) -> Union[float, Dict[str, Union[int, list]]]:
    """
    Calculate corpus-level Subtree Metric score with additional weights from embeddings
    :param hypotheses: hypotheses
    :type hypotheses: List[str]
    :param references: references
    :type references: List[str]
    :param nlp_model: one of the SpaCy NLP models with support of the DependencyParser (https://spacy.io/models)
    :type nlp_model: Language
    :param depth: depth of the subtrees to take into account
    :type depth: int
    :param make_summary: whether to make a per-sentence summary
    :type make_summary: bool
    :return: stm_package-A score
    :rtype: float
    """
    # TODO: introduce sanity checks
    score = 0

    return 1


if __name__ == '__main__':
    # Usage example
    nlp: Language = spacy.load('en_core_web_md')
    ref = 'It is a guide to action that ensures that the military will forever heed Party commands'
    hyp = 'It is a guide to action which ensures that the military always obeys the commands of the party'
    print(sentence_stm(ref,
                       hyp,
                       nlp))

    ref = 'It is a guide to action that ensures that the military will forever heed Party commands'
    hyp = 'It is to insure the troops forever hearing the activity guidebook that party direct'
    print(sentence_stm(ref,
                       hyp,
                       nlp))
