from django.urls import path
from .views import TrendingMoviesView
from .views import RecommendedMoviesView
from .views import RegisterView
from .views import FavoriteMovieView
from django.urls import path
from .views import TrendingMoviesView, RecommendedMoviesView, RegisterView, FavoriteMovieView

urlpatterns = [
    path('movies/trending/', TrendingMoviesView.as_view(), name='trending-movies'),
    path('movies/recommended/', RecommendedMoviesView.as_view(), name='recommended-movies'),
    path('movies/favorites/', FavoriteMovieView.as_view(), name='favorite-movies'),
    path('register/', RegisterView.as_view(), name='register'),
]
