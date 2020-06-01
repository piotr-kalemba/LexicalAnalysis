import re
import os
import random
from django.conf import settings
from .handle_format import pdf_to_str, get_format

COMMON_ABBR = ['a.m.', 'approx.', 'B.C.', 'cf.', 'e.g.', 'i.e.', 'Mr.', 'Mrs.', 'Ms.' 'p.a.', 'p.m.', 'St.', 'sq.',
               'Dr.', 'Prof.', 'a.k.a', 'A.D.']


def get_path(book):
    """the function returns the absolute path to the book from the library, provided it is in the media folder"""
    file_name = book.book.name
    path = os.path.join(settings.MEDIA_ROOT, file_name)
    return path


def get_content(book):
    """the function reads the content of the book and returns it as a string"""
    path = get_path(book)
    if get_format(path)[-3:] == 'pdf':
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


def how_many_words(sentence):
    """it's an auxiliary function used for measuring the length of a sentence"""
    return len(sentence.split())


def replace(string, pattern, rep, start, end):
    """ ... """
    subst = re.sub(pattern, rep, string[start:end])
    return string[:start] + subst + string[end:]


def shadow_acronyms(content):
    """ ... """
    ACRONYMS = {abbr: re.sub(r'\.', '#', abbr) for abbr in COMMON_ABBR}
    pattern = r'\w[\w.]+'
    for match_iter in re.finditer(pattern, content):
        span = match_iter.span()
        match = match_iter.group()
        if match in ACRONYMS.keys():
            content = replace(content, match, ACRONYMS[match], span[0], span[1])
    return content


def clean_sentence(sentence):
    """ ... """
    return re.sub(r'#', '.', sentence)


def get_sentences(content):
    """ ... """
    pattern = r'[A-Z][^.?!]+[.?!]'
    sentences = re.findall(pattern, content)
    sentences = [clean_sentence(sentence) for sentence in sentences]
    return sentences


def get_random_sentence(sentences):
    """the function returns a random sentence from the book content"""
    sentence = random.choice(sentences)
    return sentence


def get_common_words(lexicons):
    """the function returns a list of words that are common for all the books from the list passed as the argument"""
    common_words = lexicons[0]
    for vocabulary in lexicons[1:]:
        common_words &= vocabulary
    return list(common_words)


def get_unique_words(k, lexicons):
    """the function returns a list of words that occur in the book (first argument) but not in the contents of any other
     of the books in the list passed as the second argument"""
    total_vocab = set()
    lexicon = lexicons[k]
    n = len(lexicons)
    for i in range(n):
        if i != k:
            total_vocab |= set(lexicons[i])
    unique_words = lexicon - total_vocab
    return list(unique_words)


def get_longest_sentences(sentences, n=3):
    """the function returns the longest sentence in the content"""
    sentences.sort(key=lambda s: how_many_words(s))
    return sentences[-n:]


def sentence_len_freq(sentences):
    """the function returns a list with the distribution of the sentence lengths in the content of the book for
    sentence-length-ranges: [1,10], [11, 20], [21,30], etc"""
    sentence_len = [how_many_words(sentence) for sentence in sentences]
    max_len = max(sentence_len)
    ranges_numb = max_len // 10 + 1
    return [len([length for length in sentence_len if length in range(10 * index + 1, 10 * index + 11)]) \
            for index in range(ranges_numb)]

