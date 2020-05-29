from django.shortcuts import render, redirect
from django.views import View
from .lexical_tools import get_total_number_of_words, get_number_of_different_words, \
    get_number_of_sentences, get_longest_sentences, get_random_sentence, get_content, how_many_words, \
    sentence_len_freq, get_common_words, get_number_of_unique_words, get_path
from .forms import BookForm
from .models import Book
from .plots import FreqChart, VocabChart
import os


class UploadView(View):
    def get(self, request):
        form = BookForm()
        return render(request, 'upload.html', {'form': form})

    def post(self, request):
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            author = form.cleaned_data.get('author')
            file = form.cleaned_data.get('book')
            book = Book(title=title, author=author, book=file)
            book.save()
            return redirect('home')
        return render(request, 'upload.html', {'form': form})


class HomeView(View):
    def get(self, request):
        books = Book.objects.all()
        return render(request, 'home.html', {'books': books})

    def post(self, request):
        book_ids = request.POST.getlist('books')
        if len(book_ids) <= 1:
            return redirect('home')
        books = [Book.objects.get(id=i) for i in book_ids]
        contents = [get_content(book) for book in books]
        common = len(get_common_words(contents))
        hist = [get_number_of_unique_words(content, contents) for content in contents]
        titles = [book.title for book in books]
        chart = VocabChart()
        plot = chart.generate(titles, hist, common)
        return render(request, 'books.html', {'plot': plot})


class BookView(View):
    def get(self, request, id):
        book = Book.objects.get(id=id)
        content = get_content(book)
        word_count = int(get_total_number_of_words(content))
        different_words = int(get_number_of_different_words(content))
        sentence_count = int(get_number_of_sentences(content))
        long_sentences = get_longest_sentences(content)
        rand_sent = get_random_sentence(content)
        stl = [how_many_words(s) for s in long_sentences]
        items = list(zip(long_sentences, stl))
        context = {'word_count': word_count, 'different_words': different_words, 'sentence_count': sentence_count, \
                   'items': items, 'rand_sent': rand_sent, 'book': book}
        return render(request, 'book.html', context)


class PlotFreqView(View):
    def get(self, request, id):
        book = Book.objects.get(id=id)
        content = get_content(book)
        seq = sentence_len_freq(content)
        chart = FreqChart()
        plot = chart.generate(seq)
        return render(request, 'plot_freq.html', {'plot': plot})


class RemoveView(View):
    def get(self, request):
        books = Book.objects.all()
        return render(request, 'remove.html', {'books': books})

    def post(self, request):
        to_remove = request.POST.getlist('books')
        if to_remove:
            to_remove = [Book.objects.get(id=i) for i in to_remove]
            for book in to_remove:
                path = get_path(book)
                os.remove(path)
                book.delete()
        return redirect('remove')




