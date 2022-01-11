import logging
from functools import reduce

import spacy

DATA_TEST_LABELS = './data/test_label'
DATA_TEST_SENTENCES = './data/test_sent'
DATA_TRAIN_LABELS = './data/train_label'
DATA_TRAIN_SENTENCES = './data/train_sent'

model = spacy.load("en_core_web_sm")


def preprocessed(filename):
    sentence_file = open(filename, 'r')
    sentence_lines = sentence_file.readlines()

    def make_next(arr):
        arr.append([])
        return arr

    def add_to_current(element, arr):
        arr[-1] += [element]
        return arr

    result = reduce(lambda acc, current: make_next(acc) if current == '\n' else add_to_current(current, acc),
                    sentence_lines, [[]])
    without_whitespaces = list(map(lambda current: list(map(lambda element: element[:-1], current)), result))
    return without_whitespaces


def print_first_5(preprocessed_lines):
    first_5 = preprocessed_lines[:5]
    first_5_sentences = map(lambda arr: " ".join(arr), first_5)
    logging.info(list(first_5_sentences))


def pos_tagged(sentences):
    # print(f"Sentences are: {sentences}")
    return list(map(lambda sentence_arr: model(" ".join(sentence_arr)), sentences))


def nouns(doc):
    return list(filter(lambda token: token.pos_ == "NOUN" or token.pos_ == "PROPN", doc))


def analyse():
    preprocessed_train_sentences = preprocessed(DATA_TRAIN_SENTENCES)
    preprocessed_train_labels = preprocessed(DATA_TRAIN_LABELS)
    preprocessed_test_sentences = preprocessed(DATA_TEST_SENTENCES)
    preprocessed_test_labels = preprocessed(DATA_TEST_LABELS)

    print_first_5(preprocessed_train_sentences)
    print_first_5(preprocessed_train_labels)

    logging.info(f"NUMBER OF SENTENCES IN TRAINING SET = {len(preprocessed_train_sentences)}")
    logging.info(f"NUMBER OF SENTENCES IN TESTING SET = {len(preprocessed_test_sentences)}")
    logging.info(f"NUMBER OF LABEL LINES IN TRAINING SET = {len(preprocessed_train_labels)}")
    logging.info(f"NUMBER OF LABEL LINES IN TESTING SET = {len(preprocessed_test_labels)}")

    tagged_documents = pos_tagged(preprocessed_train_sentences + preprocessed_test_sentences)
    all_noun_tokens = reduce(lambda acc, doc: acc + nouns(doc), tagged_documents, [])

    dict = {}
    for noun_token in all_noun_tokens:
        if noun_token.lemma_ in dict.keys():
            dict[noun_token.lemma_] = dict[noun_token.lemma_] + 1
        else:
            dict[noun_token.lemma_] = 1

    noun_occurrences = list(dict.items())
    noun_occurrences.sort(reverse=True, key=lambda e: e[1])
    logging.info(f"25 Most Common Nouns Used: {noun_occurrences[:26]}")


def setup_logging():
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    logger = logging.getLogger()
    formatter = logging.Formatter('%(message)s')
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)
    logger.setLevel(logging.INFO)
    logger.addHandler(ch)


def main():
    setup_logging()
    analyse()


main()
