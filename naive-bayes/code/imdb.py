import getopt
import logging
import math
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import BernoulliNB
from sklearn import metrics

EXPOSURE_AT_DEFAULT = "Exposure at Default (in lakh Rs.)"
RECOVERY_PERCENTAGE = "Recovery (%)"
PROBABILITY_OF_DEFAULT = "Probability of Default"

training_reviews = pd.read_csv("../data/movie_review_train.csv")
test_reviews = pd.read_csv("../data/movie_review_test.csv")

print(training_reviews.columns)

CLASS = "class"
POSITIVE = "Pos"
NEGATIVE = "Neg"

review_mapping = dict(zip([POSITIVE, NEGATIVE], [1, 0]))
print(training_reviews[CLASS].unique())
training_reviews[CLASS] = training_reviews[CLASS].map(review_mapping)
print(training_reviews[CLASS].unique())

training_texts = training_reviews.values[:, 1]
training_ratings = training_reviews.values[:, 0].astype('int')

vectorizer = CountVectorizer(stop_words="english", min_df=0.03, max_df=0.8)
vectorizer.fit(training_texts)

print(len(vectorizer.vocabulary_))
# print(vectorizer.get_feature_names())
sparse_training_texts = vectorizer.transform(training_texts)

# naive_bayes_classifier = MultinomialNB()
naive_bayes_classifier = BernoulliNB()

naive_bayes_classifier.fit(sparse_training_texts, training_ratings)

test_reviews[CLASS] = test_reviews[CLASS].map(review_mapping)
test_texts = training_reviews.values[:, 1]
test_ratings = training_reviews.values[:, 0].astype('int')
sparse_test_texts = vectorizer.transform(test_texts)
# print(f"Test shape= {sparse_test_texts.nonzero()}")
predictions = naive_bayes_classifier.predict(sparse_test_texts)
probabilities = naive_bayes_classifier.predict_proba(sparse_test_texts)
print(predictions)
print(probabilities)

print(naive_bayes_classifier)

print(metrics.accuracy_score(test_ratings, predictions))
confusion_matrix = metrics.confusion_matrix(test_ratings, predictions)
print(confusion_matrix)
