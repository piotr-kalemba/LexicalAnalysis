import re
import os
import random


def all_books(path):
    return [filename for filename in os.listdir(path) if filename.endswith('.txt')]


def get_path(book):
    path = os.getcwd()
    path += f'/LexicalApp/library/{book}'
    return path


def get_all_words(book):
    """the function returns a list of all running words in the content (with duplicates)"""
    path = get_path(book)
    with open(path, 'r') as f:
        content = f.read().lower()
        words = re.findall(r'\b([\w]+-?)+\b', content)
        # the pattern for a word above matches strings like 'Alice', 'English-speaking', 'merry-go-round' but does not
        # match '-', '--', non-alphanumeric strings, ect
    return words


def get_total_number_of_words(book):
    """the function returns the number of running words in the content"""
    return len(get_all_words(book))


def get_different_words(book):
    """the function returns a list of words in the content without duplicates"""
    return list(set(get_all_words(book)))


def get_number_of_different_words(book):
    """the function returns the number of words in the content"""
    return len(get_different_words(book))


def how_many_words(sentence):
    """it's an auxiliary function used for measuring the length of a sentence"""
    return len(sentence.split())


def get_all_sentences(book):
    """the function returns a list of all sentences in the content"""
    path = get_path(book)
    with open(path, 'r') as f:
        content = f.read()
        sentences = re.findall(r'[A-Z][^.?!]+[.?!]', content)
    return sentences


def get_random_sentence(book):
    """the function returns a random sentence from the book content"""
    sentences = get_all_sentences(book)
    sentence = random.choice(sentences)
    return sentence


def get_common_words(books):
    """the function returns a list of words that are common for all the books from the list passed as the argument"""
    common_words = set(get_all_words(books[0]))
    for book in books[1:]:
        common_words &= set(get_all_words(book))

    return list(common_words)


def get_unique_words(book, books):
    """the function returns a list of words that occur in the book (first argument) but not in the contents of any other
     of the books in the list passed as the second argument"""
    total_vocab = set()
    for item in books:
        if item != book:
            total_vocab |= set(get_all_words(item))
    unique_words = set(get_all_words(book)) - total_vocab

    return list(unique_words)


def get_number_of_sentences(book):
    """the function returns the number of sentences in the content of the book"""
    return len(get_all_sentences(book))


def get_longest_sentence(book):
    """the function returns the longest sentence in the content of the book"""
    sentences = get_all_sentences(book)
    longest = max([how_many_words(sentence) for sentence in sentences])
    for sentence in sentences:
        if how_many_words(sentence) == longest:
            return sentence


def sentence_len_freq(book):
    """the function returns a list with the distribution of the sentence lengths in the content of the book for
    sentence-length-ranges: [1,10], [11, 20], [21,30], etc"""
    sentences = get_all_sentences(book)
    sentence_len = [how_many_words(sentence) for sentence in sentences]
    max_len = max(sentence_len)
    ranges_numb = max_len // 10 + 1

    return [len([length for length in sentence_len if length in range(10 * index + 1, 10 * index + 11)])\
            for index in range(ranges_numb)]

