from django.urls import path
from .views import TrendingMoviesView
from .views import RecommendedMoviesView
from .views import RegisterView
from .views import FavoriteMovieView



urlpatterns = [
    path('trending/', TrendingMoviesView.as_view(), name='trending-movies'),
    path('recommended/', RecommendedMoviesView.as_view(), name='recommended-movies'),
    path('register/', RegisterView.as_view(), name='register'),
    path('favorites/', FavoriteMovieView.as_view(), name='favorite-movies'),
]
