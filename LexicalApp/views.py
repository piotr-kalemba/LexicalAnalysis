from django.shortcuts import render
from django.views import View
from . lexical_tools import get_total_number_of_words, get_number_of_different_words, \
    get_number_of_sentences, get_longest_sentence, get_random_sentence
from . manage_library import get_books, get_book, get_title


class IndexView(View):
    def get(self, request):
        books = get_books()
        titles = [" ".join(book[:-4].split('_')).title() for book in books]
        titles = zip(titles, range(len(titles)))
        return render(request, 'index.html', {'books': titles})


class BookView(View):
    def get(self, request, id):
        book = get_book(id)
        title = get_title(id)
        x1 = str(get_total_number_of_words(book))
        x2 = str(get_number_of_different_words(book))
        x3 = str(get_number_of_sentences(book))
        long_sent = get_longest_sentence(book)
        context = {'word_count': x1, 'different_words': x2, 'sentence_count': x3, \
                   'long_sent': long_sent, 'title': title, 'id': id}
        return render(request, 'book.html', context)


class RandomSentence(View):
    def get(self, request, id):
        book = get_book(id)
        sentence = get_random_sentence(book)
        return render(request, 'random.html', {'sentence': sentence, 'id': id})


