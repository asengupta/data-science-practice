import spacy
import sklearn_crfsuite
from sklearn_crfsuite import metrics
from functools import reduce

model = spacy.load("en_core_web_sm")

print("Test")
file = open('./data/test_sent', 'r')
lines = file.readlines()

# print(lines)

arr = []
def build(arr):
    def make_next():
        arr.append([])
        return arr
    def add_to_current(element):
        arr[-1] += [element]
        return arr
    make_next()
    return make_next, add_to_current

make_next, add_to_current = build([])

result = reduce(lambda acc, current: make_next() if current == '\n' else add_to_current(current), lines, [])
# result = reduce(lambda split, current: split + [current], lines, [])
# print(result)

print(result)
# print(make_next)
# print(add_to_current)
# index = 0
# for line in lines:
#     if line == '\n':
