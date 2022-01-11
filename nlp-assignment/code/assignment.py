from functools import reduce

import spacy
import getopt
import logging
import sys

model = spacy.load("en_core_web_sm")


def preprocessed(filename):
    global make_next, add_to_current
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

def analyse():
    preprocessed_train_sentences = preprocessed('./data/train_sent')
    preprocessed_train_labels = preprocessed('./data/train_label')
    preprocessed_test_sentences = preprocessed('./data/test_sent')
    preprocessed_test_labels = preprocessed('./data/test_label')

    print_first_5(preprocessed_train_sentences)
    print_first_5(preprocessed_train_labels)

    logging.info(f"NUMBER OF SENTENCES IN TRAINING SET = {len(preprocessed_train_sentences)}")
    logging.info(f"NUMBER OF SENTENCES IN TESTING SET = {len(preprocessed_test_sentences)}")
    logging.info(f"NUMBER OF LABEL LINES IN TRAINING SET = {len(preprocessed_train_labels)}")
    logging.info(f"NUMBER OF LABEL LINES IN TESTING SET = {len(preprocessed_test_labels)}")

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
