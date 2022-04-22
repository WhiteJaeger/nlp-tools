import nltk
import re
from nltk.tokenize.toktok import ToktokTokenizer

from constants import CONTRACTION_MAP

stopword_list = nltk.corpus.stopwords.words('english')
stopword_list.remove('no')
stopword_list.remove('not')


def prepare_text(text: str,
                 contraction_expansion=True,
                 lowercase=False,
                 remove_spec_characters=True,
                 filter_stopwords=False,
                 remove_digits=False) -> str:
    """
    Preprocess the given string
    """
    # expand contractions
    if contraction_expansion:
        text = expand_contractions(text)

    # lowercase the text
    if lowercase:
        text = text.lower()

    # remove special characters and\or digits
    if remove_spec_characters:
        # insert spaces between special characters to isolate them
        special_char_pattern = re.compile(r'([{.(-)!}])')
        text = special_char_pattern.sub(" \\1 ", text)
        text = remove_special_characters(text, remove_digits=remove_digits)
        # remove extra whitespace
        text = re.sub(r'\s+', ' ', text)

    # remove stopwords
    if filter_stopwords:
        text = remove_stopwords(text, is_lower_case=lowercase)

    return text


def prepare_sentence_for_pos_tagging(sentence: str) -> dict:
    result = {
        'cleared_sentence': None,
        'pos_tagging_ready_sentence': None
    }

    sentence = prepare_text(text=sentence, contraction_expansion=True, lowercase=True, remove_spec_characters=True,
                            remove_digits=True)
    result['cleared_sentence'] = sentence

    text = [sentence.split()]
    prepared_text = []
    for sentence_ in text:
        prepared_text.append([encode_word(sentence_, w_index) for w_index in range(len(sentence_))])

    result['pos_tagging_ready_sentence'] = prepared_text
    return result


def map_word_to_pos(prepared_sentence: str, pos_tags: list) -> list:
    words = prepared_sentence.split()

    mapped = zip(words, pos_tags)

    return list(mapped)


def expand_contractions(text, contraction_mapping=CONTRACTION_MAP):
    """
    Utils function to transform contractions into the normalized format.
    Example usage:
        input_text = 'Y'all can't expand contractions I'd think'
        print(expand_contractions(input_text))
        Output: `You all cannot expand contractions I would think`
    """
    contractions_pattern = re.compile('({})'.format('|'.join(contraction_mapping.keys())),
                                      flags=re.IGNORECASE | re.DOTALL)

    def expand_match(contraction):
        match = contraction.group(0)
        first_char = match[0]
        expanded_contraction = contraction_mapping.get(match) \
            if contraction_mapping.get(match) \
            else contraction_mapping.get(match.lower())
        expanded_contraction = first_char + expanded_contraction[1:]
        return expanded_contraction

    expanded_text = contractions_pattern.sub(expand_match, text)
    expanded_text = re.sub("'", "", expanded_text)
    return expanded_text


def remove_special_characters(text: str, remove_digits=False) -> str:
    """
    Utils function to remove special characters.
    """
    pattern = r'[^a-zA-z0-9\s]' if not remove_digits else r'[^a-zA-z\s]'
    text = re.sub(pattern, '', text)
    return text


def remove_stopwords(text: str, is_lower_case: bool = False) -> str:
    tokenizer = ToktokTokenizer()
    tokens = tokenizer.tokenize(text)
    tokens = [token.strip() for token in tokens]
    if is_lower_case:
        filtered_tokens = [token for token in tokens if token not in stopword_list]
    else:
        filtered_tokens = [token for token in tokens if token.lower() not in stopword_list]
    filtered_text = ' '.join(filtered_tokens)
    return filtered_text


def encode_word(sentence: list, word_index: int) -> dict:
    """
    Function to encode a single word in the given sentence.
    :param sentence: list of words: [word1, word2, word3 etc.]
    :type sentence: list
    :param word_index: position of the word in the sentence
    :type word_index: int
    :return: representation of a word as its features
    :rtype: dict
    """

    # If the given word is None or empty str -> return special tag
    if not sentence[word_index]:
        return {
            'Not-a-word': 1
        }

    return {
        'is_first_capital': int(sentence[word_index][0].isupper()),
        'is_first_word': int(word_index == 0),
        'is_last_word': int(word_index == len(sentence) - 1),
        'is_complete_capital': int(sentence[word_index].upper() == sentence[word_index]),
        # Consider the information in the prev word
        'prev_word': '' if word_index == 0 else sentence[word_index - 1],
        # Consider the information in the next word
        'next_word': '' if word_index == len(sentence) - 1 else sentence[word_index + 1],
        'is_numeric': int(sentence[word_index].isdigit()),
        # For ABC123 cases
        'is_alphanumeric': int(bool((re.match('^(?=.*[0-9]$)(?=.*[a-zA-Z])', sentence[word_index])))),
        # Extracting the morphological info of the given word
        'prefix_1': sentence[word_index][0],
        'prefix_2': sentence[word_index][:2],
        'prefix_3': sentence[word_index][:3],
        'prefix_4': sentence[word_index][:4],
        'suffix_1': sentence[word_index][-1],
        'suffix_2': sentence[word_index][-2:],
        'suffix_3': sentence[word_index][-3:],
        'suffix_4': sentence[word_index][-4:],
        'word_has_hyphen': 1 if '-' in sentence[word_index] else 0
    }
