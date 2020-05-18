from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.HomeView.as_view(), name='home'),
    path('upload/', views.UploadView.as_view(), name='upload'),
    path('book/<int:id>', views.BookView.as_view(), name='book'),
    path('plot/<int:id>', views.PlotView.as_view(), name='plot'),
]