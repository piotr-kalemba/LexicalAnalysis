from . lexical_tools import all_books
import os


def get_books():
    path = os.getcwd()
    path += '/LexicalApp/library'
    books = all_books(path)
    return books


def get_book(id):
    books = get_books()
    book = books[id]
    return book


def get_title(id):
    book = get_book(id)
    return " ".join(book[:-4].split('_')).title()

