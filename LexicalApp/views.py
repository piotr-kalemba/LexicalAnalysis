from django.shortcuts import render, redirect
from django.views import View
from . lexical_tools import get_total_number_of_words, get_number_of_different_words, \
    get_number_of_sentences, get_longest_sentences, get_random_sentence, get_content, how_many_words
from .forms import BookForm
from .models import Book
from .plots import create_bar_freq
import io
import urllib, base64


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
        content = get_content(book)
        word_count = int(get_total_number_of_words(content))
        different_words = int(get_number_of_different_words(content))
        sentence_count = int(get_number_of_sentences(content))
        long_sentences = get_longest_sentences(content)
        rand_sent = get_random_sentence(content)
        s1, s2, s3 = long_sentences
        s_len = how_many_words
        l1, l2, l3 = s_len(s1), s_len(s2), s_len(s3)
        context = {'word_count': word_count, 'different_words': different_words, 'sentence_count': sentence_count, \
                   'l1': l1, 'l2': l2, 'l3': l3, 's1': s1, 's2': s2, 's3': s3, 'rand_sent': rand_sent, 'book': book}
        return render(request, 'book.html', context)


class PlotView(View):
    def get(self, request, id):
        book = Book.objects.get(id=id)
        create_bar_freq(book)
        return redirect('home')



