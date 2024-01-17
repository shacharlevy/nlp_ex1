import json
import nltk
from collections import defaultdict
import string
import pickle
import os.path
nltk.download('punkt')


def split_text_to_sentences(file_path):
    formatted_sentences = []

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            cleaned_line = line.translate(str.maketrans('', '', string.punctuation))
            formatted_sentences.append(f"<s> {cleaned_line.strip()} </s>")

    return formatted_sentences


def get_words_and_bigrams_frequencies(sentences, lexicon_words):
    words_freq = defaultdict(int)
    bigrams_freq = defaultdict(dict)

    for sentence in sentences:
        for i, word in enumerate(sentence):
            if word in lexicon_words:
                words_freq[word] += 1
            if i < len(sentence) - 1:
                if sentence[i] in lexicon_words and sentence[i + 1] in lexicon_words:
                    bigrams_freq[sentence[i]][sentence[i + 1]] += 1

    return words_freq, bigrams_freq


def get_2grams_statistics(corpus_path, lexicon_path):
    bigrams_prob = defaultdict(dict)

    with open(lexicon_path, 'r', encoding='utf-8') as lexicon_file:
        lexicon_content = lexicon_file.read()

    lexicon_words = set(lexicon_content.split())
    lexicon_words.add('<s>')
    lexicon_words.add('</s>')

    sentences = split_text_to_sentences(corpus_path)
    words_freq, bigrams_freq = get_words_and_bigrams_frequencies(sentences, lexicon_words)

    total_words = sum([len(sentence.split()) for sentence in sentences])

    for word1 in bigrams_freq:
        for word2 in bigrams_freq[word1]:
            prob_word1 = words_freq[word1] / total_words
            prob_word2_given_word1 = (bigrams_freq[word1][word2] / (total_words - 1)) / prob_word1
            bigrams_prob[word1][word2] = prob_word1 * prob_word2_given_word1

    return bigrams_prob



# def get_2grams_statistics(corpus, lexicon):
#     bigrams_prob = defaultdict(float)
#     sentences = split_text_to_sentences(corpus)
#     lexicon_words = set(lexicon.split())
#     lexicon_words.add('<s>')
#     lexicon_words.add('</s>')
#     words_freq, bigrams_freq = get_words_and_bigrams_frequencies(sentences, lexicon_words)
#
#     total_words = sum([len(sentence) for sentence in sentences])
#
#     for sentence in sentences:
#         for i in range(1, len(sentence)):
#             if sentence[i - 1] in lexicon_words and sentence[i] in lexicon_words:
#                 bigram = f"{sentence[i - 1]} {sentence[i]}"
#                 prob_word1 = words_freq[sentence[i - 1]] / total_words
#                 prob_word2_given_word1 = (bigrams_freq[bigram] / (total_words - 1)) / prob_word1
#                 bigrams_prob[bigram] = prob_word1 * prob_word2_given_word1
#
#     return bigrams_prob


def get_max_prob_word(tokens, i, candidates, bigrams_statistics):
    max_prob = 0
    element = candidates.pop()
    res = element
    candidates.add(element)

    for candidate in candidates:
        prob = bigrams_statistics[tokens[i - 1]][candidate] * bigrams_statistics[candidate][tokens[i + 1]]
        if prob > max_prob:
            max_prob = prob
            res = candidate

    return res


def solve_cloze(input, candidates, lexicon, corpus):
    # todo: implement this function
    print(f'starting to solve the cloze {input} with {candidates} using {lexicon} and {corpus}')
    formatted_sentences = split_text_to_sentences(input)
    if not os.path.isfile('bigrams_statistics.pkl'):
        bigrams_statistics = get_2grams_statistics(corpus, lexicon)
        pickle.dump(bigrams_statistics, open('bigrams_statistics.pkl', 'wb'))
    else:
        bigrams_statistics = pickle.load(open('bigrams_statistics.pkl', 'rb'))
    with open(candidates, 'r', encoding='utf-8') as candidates_file:
        candidates_text = candidates_file.read()
    candidates = set(candidates_text.split())

    solutions = []

    for sentence in formatted_sentences:
        tokens = sentence.split()

        for i in range(1, len(tokens) - 1):
            curr_token = tokens[i]

            if curr_token[0] == '_':
                pred_word = get_max_prob_word(tokens, i, candidates, bigrams_statistics)
                candidates.remove(pred_word)
                solutions.append(pred_word)

    return solutions


if __name__ == '__main__':
    with open('config.json', 'r') as json_file:
        config = json.load(json_file)

    solution = solve_cloze(config['input_filename'],
                           config['candidates_filename'],
                           config['lexicon_filename'],
                           config['corpus'])

    print('cloze solution:', solution)
