import re
import os
import random
from django.conf import settings
from .handle_format import pdf_to_str, get_format

COMMON_ABBR = ['approx.', 'cf.', 'Mr.', 'Mrs.', 'Ms.', 'St.', 'sq.', 'Dr.', 'Prof.']


def get_path(book):
    """function returns the absolute path to the book from the library, provided it is in the media folder"""
    file_name = book.book.name
    path = os.path.join(settings.MEDIA_ROOT, file_name)
    return path


def get_content(book):
    """function reads the content of the book and returns it as a string"""
    path = get_path(book)
    if get_format(path)[-3:] == 'pdf':
        content = pdf_to_str(path)
    else:
        with open(path, 'r') as f:
            content = f.read()
    return content


def get_all_words(content):
    """function returns a list of all running words in the content (with duplicates)"""
    content = content.lower()
    words = re.findall(r'\b([\w]+-?)+\b', content)
    # the pattern for a word above matches strings like 'Alice', 'English-speaking', 'merry-go-round' but does not
    # match '-', '--', non-alphanumeric strings, ect
    return words


def how_many_words(sentence):
    """an auxiliary function used for measuring the length of a sentence"""
    return len(sentence.split())


def substitute(string, to_sub, sub_by, start, end):
    """an auxiliary function that replaces every occurrence of to_sub for sub_by in the string between
    start and end indices"""
    subst = string[start:end].replace(to_sub, sub_by)
    return string[:start] + subst + string[end:]


def handle_acronyms(content):
    """function tries to find all acronyms in the content and shadow periods in them so that they will not be
    confused with full stops ending sentences"""
    pattern = r"\w\.\w(\.\w?)*"
    for item in re.finditer(pattern, content):
        span = item.span()
        content = substitute(content, ".", "@", span[0], span[1])

    pattern = r"\w+\."
    ACRONYMS = {acr: acr.replace(".", "@") for acr in COMMON_ABBR}
    for itermatch in re.finditer(pattern, content):
        span = itermatch.span()
        match = itermatch.group()
        if match in ACRONYMS.keys():
            content = substitute(content, match, ACRONYMS[match], span[0], span[1])

    return content


def clean_sentence(sentence):
    """function replaces shadowed punctuation marks back to the original marks"""
    sentence = sentence.replace('@', '.')
    return sentence


def get_sentences(content):
    """function tries to find all sentences in the content; it draws on previous auxiliary functions to exclude
    some false positives"""
    content = handle_acronyms(content)
    pattern = r'[A-Z][^.?!]+[.?!]'
    sentences = re.findall(pattern, content)
    sentences = [clean_sentence(sentence) for sentence in sentences]
    return sentences


def get_random_sentence(sentences):
    """function returns a random sentence from the book content"""
    sentence = random.choice(sentences)
    return sentence


def get_common_words(lexicons):
    """function returns a list of words that are common for all the books from the list passed as the argument"""
    common_words = set(lexicons[0][:])
    for vocabulary in lexicons[1:]:
        common_words &= set(vocabulary)
    return list(common_words)


def get_unique_words(k, lexicons):
    """function returns a list of words that occur in the book (first argument) but not in the contents of any other
     of the books in the list passed as the second argument"""
    total_vocab = set()
    lexicon = set(lexicons[k])
    n = len(lexicons)
    for i in range(n):
        if i != k:
            total_vocab |= set(lexicons[i])
    unique_words = lexicon - total_vocab
    return list(unique_words)


def get_longest_sentences(sentences, n=3):
    """function returns the longest sentence in the content"""
    sentences.sort(key=lambda s: how_many_words(s))
    return sentences[-n:]


def sentence_len_freq(sentences):
    """function returns a list with the distribution of the sentence lengths in the content of the book for
    sentence-length-ranges: [1,10], [11, 20], [21,30], etc"""
    sentence_len = [how_many_words(sentence) for sentence in sentences]
    max_len = max(sentence_len)
    ranges_numb = max_len // 10 + 1
    return [len([length for length in sentence_len if length in range(10 * index + 1, 10 * index + 11)]) \
            for index in range(ranges_numb)]

