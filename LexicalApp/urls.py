from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.IndexView.as_view(), name='index'),
    path('book/<int:id>', views.BookView.as_view(), name='book'),
    path('random/<int:id>', views.RandomSentence.as_view(), name='random'),
]