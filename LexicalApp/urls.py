from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('upload/', views.UploadView.as_view(), name='upload'),
    path('book/<int:id>', views.BookView.as_view(), name='book'),
    path('plot_freq/<int:id>', views.PlotFreqView.as_view(), name='plot-freq'),
    path('remove/', views.RemoveView.as_view(), name='remove'),
    path('book/<int:id>/<int:num>', views.BookSentView.as_view(), name='book-sent'),
]