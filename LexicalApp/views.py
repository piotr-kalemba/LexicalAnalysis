from django.shortcuts import render, redirect
from django.views import View
from .lexical_tools import get_all_words, get_longest_sentences, get_random_sentence, get_content, how_many_words, \
    sentence_len_freq, get_common_words, get_path, get_sentences, get_unique_words, suffix
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
        lexicons = [list(set(get_all_words(get_content(book)))) for book in books]
        common = len(get_common_words(lexicons))
        unique = [len(get_unique_words(k, lexicons)) for k in range(len(lexicons))]
        shared = [len(lexicons[k]) - (common + unique[k]) for k in range(len(lexicons))]
        titles = [book.title for book in books]
        chart = VocabChart()
        plot = chart.generate(titles, unique, shared, common)
        return render(request, 'books.html', {'plot': plot})


class BookView(View):
    def get(self, request, id):
        book = Book.objects.get(id=id)
        content = get_content(book)
        words = get_all_words(content)
        sentences = get_sentences(content)
        stats = [0] * 4
        stats[0] = len(words)
        stats[1] = len(set(words))
        stats[2] = len(sentences)
        stats[3] = stats[0] // stats[2]
        long_sentences = get_longest_sentences(sentences)
        rand_sent = get_random_sentence(sentences)
        sentence = long_sentences[-1]
        size = how_many_words(sentence)
        context = {'stats': stats, 'sentence': sentence, 'rand_sent': rand_sent, 'book': book, 'size': size}
        return render(request, 'book.html', context)


class BookSentView(View):
    def post(self, request, id, num):
        book = Book.objects.get(id=id)
        content = get_content(book)
        words = get_all_words(content)
        sentences = get_sentences(content)
        stats = [0] * 4
        stats[0] = len(words)
        stats[1] = len(set(words))
        stats[2] = len(sentences)
        stats[3] = stats[0] // stats[2]
        long_sentences = get_longest_sentences(sentences)
        rand_sent = get_random_sentence(sentences)
        num %= 100
        num += 1
        sentence = long_sentences[-num]
        size = how_many_words(sentence)
        suf = suffix(num, size)
        context = {'stats': stats, 'sentence': sentence, 'rand_sent': rand_sent, 'book': book, 'size': size,
                   'num': num, 'suf': suf}
        return render(request, 'book_sent.html', context)


class PlotFreqView(View):
    def get(self, request, id):
        book = Book.objects.get(id=id)
        content = get_content(book)
        sentences = get_sentences(content)
        seq = sentence_len_freq(sentences)
        chart = FreqChart(book.title)
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
