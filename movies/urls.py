from django.urls import path
from .views import TrendingMoviesView
from .views import RecommendedMoviesView

urlpatterns = [
    path('trending/', TrendingMoviesView.as_view(), name='trending-movies'),
    path('recommended/', RecommendedMoviesView.as_view(), name='recommended-movies'),
]
