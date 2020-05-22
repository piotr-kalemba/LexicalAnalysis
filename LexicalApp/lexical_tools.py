import re
import os
import random
from django.conf import settings
from .handle_format import pdf_to_str


def get_path(book):
    """the function returns the absolute path to the book from the library, provided it is in the media folder"""
    file_name = book.book.name
    path = os.path.join(settings.MEDIA_ROOT, file_name)
    return path


def get_content(book):
    """the function reads the content of the book and returns it as a string"""
    path = get_path(book)
    ext = book.book.name.split('.')[-1]
    if ext.lower() == 'pdf':
        content = pdf_to_str(path)
    else:
        with open(path, 'r') as f:
            content = f.read()
    return content


def get_all_words(content):
    """the function returns a list of all running words in the content (with duplicates)"""
    content = content.lower()
    words = re.findall(r'\b([\w]+-?)+\b', content)
    # the pattern for a word above matches strings like 'Alice', 'English-speaking', 'merry-go-round' but does not
    # match '-', '--', non-alphanumeric strings, ect
    return words


def get_total_number_of_words(content):
    """the function returns the number of running words in the content"""
    return len(get_all_words(content))


def get_different_words(content):
    """the function returns a list of words in the content without duplicates"""
    return list(set(get_all_words(content)))


def get_number_of_different_words(content):
    """the function returns the number of words in the content"""
    return len(get_different_words(content))


def how_many_words(sentence):
    """it's an auxiliary function used for measuring the length of a sentence"""
    return len(sentence.split())


def get_all_sentences(content):
    """the function returns a list of all sentences in the content"""
    sentences = re.findall(r'[A-Z][^.?!]+[.?!]', content)
    return sentences


def get_random_sentence(content):
    """the function returns a random sentence from the book content"""
    sentences = get_all_sentences(content)
    sentence = random.choice(sentences)
    return sentence


def get_common_words(contents):
    """the function returns a list of words that are common for all the books from the list passed as the argument"""
    common_words = set(get_all_words(contents[0]))
    for content in contents[1:]:
        common_words &= set(get_all_words(content))
    return list(common_words)


def get_unique_words(content, contents):
    """the function returns a list of words that occur in the book (first argument) but not in the contents of any other
     of the books in the list passed as the second argument"""
    total_vocab = set()
    for item in contents:
        if item != content:
            total_vocab |= set(get_all_words(item))
    unique_words = set(get_all_words(content)) - total_vocab
    return list(unique_words)


def get_number_of_unique_words(content, contents):
    """the function returns the number of unique words in content but not in contents"""
    return len(get_unique_words(content, contents))


def get_number_of_sentences(content):
    """the function returns the number of sentences in the content of the book"""
    return len(get_all_sentences(content))


def get_longest_sentences(content, n=3):
    """the function returns the longest sentence in the content"""
    sentences = get_all_sentences(content)
    sentences.sort(key=lambda s: how_many_words(s))
    return sentences[-n:]


def sentence_len_freq(content):
    """the function returns a list with the distribution of the sentence lengths in the content of the book for
    sentence-length-ranges: [1,10], [11, 20], [21,30], etc"""
    sentences = get_all_sentences(content)
    sentence_len = [how_many_words(sentence) for sentence in sentences]
    max_len = max(sentence_len)
    ranges_numb = max_len // 10 + 1
    return [len([length for length in sentence_len if length in range(10 * index + 1, 10 * index + 11)])\
            for index in range(ranges_numb)]
