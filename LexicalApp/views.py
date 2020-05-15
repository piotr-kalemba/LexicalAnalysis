from django.shortcuts import render, redirect
from django.views import View
from . lexical_tools import get_total_number_of_words, get_number_of_different_words, \
    get_number_of_sentences, get_longest_sentence, get_random_sentence
from .forms import BookForm
from .models import Book


class UploadView(View):
    def get(self, request):
        form = BookForm()
        return render(request, 'upload.html', {'form': form})

    def post(self, request):
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')


class HomeView(View):
    def get(self, request):
        books = Book.objects.all()
        return render(request, 'home.html', {'books': books})


class BookView(View):
    def get(self, request, id):
        book = Book.objects.get(id=id)
        word_count = int(get_total_number_of_words(book))
        different_words = int(get_number_of_different_words(book))
        sentence_count = int(get_number_of_sentences(book))
        long_sent = get_longest_sentence(book)
        context = {'word_count': word_count, 'different_words': different_words, 'sentence_count': sentence_count, \
                   'long_sent': long_sent}
        return render(request, 'book.html', context)


class RandomSentence(View):
    pass


