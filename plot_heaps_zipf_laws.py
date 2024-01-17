import json
import pickle
import os.path
from collections import defaultdict
from matplotlib import pyplot as plt
from math import log
from nltk.stem import WordNetLemmatizer
import nltk
import seaborn as sn
sn.set()
nltk.download('wordnet')


def read_data(filename, batch_size=100000):
    tokens2types = defaultdict(int)
    types = set()
    tokens = 0
    lemmatizer = WordNetLemmatizer()

    with open(filename, 'r', encoding='utf-8', errors='replace') as fin:
        print('Reading the text file...')
        for i, line in enumerate(fin):
            words = line.split()
            for word in words:
                lemma = lemmatizer.lemmatize(word, pos='v')
                types.add(lemma)
            tokens += len(words)

            if i % batch_size == 0 and i != 0:
                tokens2types[tokens] = len(types)
                print(f'Processed {i} lines')
                # Reset the counts for the next batch
                types.clear()

    return tokens2types
# def read_data(filename):
#     word2freq = defaultdict(int)
#
#     with open(filename, 'r',  encoding='utf-8', errors='replace') as fin:
#         print('reading the text file...')
#         for i, line in enumerate(fin):
#             for word in line.split():
#                 word2freq[word] += 1
#             if i % 100000 == 0:
#                 print(i)
#
#     total_words = sum(word2freq.values())
#     word2nfreq = {w: word2freq[w]/total_words for w in word2freq}
#
#     return word2nfreq

def read_data(filename, batch_size=100000):
    tokens2types = defaultdict(int)
    types = set()
    tokens = 0
    lemmatizer = WordNetLemmatizer()

    with open(filename, 'r', encoding='utf-8', errors='replace') as fin:
        print('Reading the text file...')
        for i, line in enumerate(fin):
            words = line.split()
            for word in words:
                lemma = lemmatizer.lemmatize(word, pos='v')
                types.add(lemma)
            tokens += len(words)

            if i % batch_size == 0 and i != 0:
                tokens2types[tokens] = len(types)
                print(f'Processed {i} lines')
    return tokens2types


def plot_zipf_law(tokens2types):
    y = sorted(tokens2types.values(), reverse=True)
    x = list(range(1, len(y)+1))

    product = [a * b for a, b in zip(x, y)]
    print(product[:1000])  # todo: print and note the roughly constant value

    y = [log(e, 2) for e in y]
    x = [log(e, 2) for e in x]

    plt.plot(x, y)
    plt.xlabel('log(rank)')
    plt.ylabel('log(frequency)')
    plt.title("Zipf's law")
    plt.show()

def plot_heap_law(tokens2types):
    y = list(tokens2types.values())
    x = list(tokens2types.keys())

    plt.plot(x, y)
    plt.xlabel('Tokens')
    plt.ylabel('Types')
    plt.title("Heap's Law")
    plt.show()

if __name__ == '__main__':
    with open('config.json', 'r') as json_file:
        config = json.load(json_file)

    if not os.path.isfile('tokens2types.pkl'):
        data = read_data(config['corpus'])
        pickle.dump(data, open('tokens2types.pkl', 'wb'))

    plot_heap_law(pickle.load(open('tokens2types.pkl', 'rb')))

