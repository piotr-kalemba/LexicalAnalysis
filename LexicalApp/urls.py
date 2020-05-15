from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.HomeView.as_view(), name='home'),
    path('upload/', views.UploadView.as_view(), name='upload'),
    path('book/<int:id>', views.BookView.as_view(), name='book'),
    # path('random/<int:id>', views.RandomSentence.as_view(), name='random'),
]