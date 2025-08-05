import requests
from django.conf import settings
from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import FavoriteMovie
from .serializers import RegisterSerializer, FavoriteMovieSerializer


# -------------------------
#  TRENDING MOVIES
# -------------------------
class TrendingMoviesView(APIView):
    def get(self, request):
        cache_key = "trending_movies"
        cached_data = cache.get(cache_key)

        if cached_data:
            return Response(cached_data)

        print("Fetching trending movies from TMDb")
        url = "https://api.themoviedb.org/3/trending/movie/week"
        params = {"api_key": settings.TMDB_API_KEY}

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json().get('results', [])
            cache.set(cache_key, data, timeout=60 * 10)  # cache for 10 minutes
            return Response(data)
        except requests.RequestException:
            return Response({"error": "Failed to fetch trending movies"}, status=500)


# -------------------------
#  RECOMMENDED MOVIES (Top Rated)
# -------------------------
class RecommendedMoviesView(APIView):
    def get(self, request):
        cache_key = "recommended_movies"
        cached_data = cache.get(cache_key)

        if cached_data:
            return Response(cached_data)

        print("Fetching recommended movies from TMDb")
        url = "https://api.themoviedb.org/3/movie/top_rated"
        params = {"api_key": settings.TMDB_API_KEY}

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json().get('results', [])[:10]  # top 10
            cache.set(cache_key, data, timeout=60 * 10)  # cache 10 minutes
            return Response(data)
        except requests.RequestException:
            return Response({"error": "Failed to fetch recommended movies"}, status=500)


# -------------------------
#  USER REGISTRATION
# -------------------------
class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# -------------------------
#  FAVORITE MOVIES
# -------------------------
class FavoriteMovieView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        favorites = FavoriteMovie.objects.filter(user=request.user)
        serializer = FavoriteMovieSerializer(favorites, many=True)
        return Response(serializer.data)

    def post(self, request):
        """Save a movie to favorites using only TMDB movie ID."""
        tmdb_id = request.data.get('tmdb_id')
        if not tmdb_id:
            return Response({"error": "tmdb_id is required"}, status=400)

        # Fetch movie details from TMDB
        url = f"https://api.themoviedb.org/3/movie/{tmdb_id}"
        params = {"api_key": settings.TMDB_API_KEY}
        response = requests.get(url, params=params)

        if response.status_code != 200:
            return Response({"error": "Failed to fetch movie from TMDB"}, status=400)

        movie_data = response.json()

        # Save favorite movie
        favorite, created = FavoriteMovie.objects.get_or_create(
            user=request.user,
            tmdb_id=tmdb_id,
            defaults={
                "title": movie_data.get("title"),
                "poster_path": movie_data.get("poster_path"),
                "release_date": movie_data.get("release_date"),
            }
        )

        return Response({
            "message": "Added to favorites" if created else "Already in favorites",
            "movie": movie_data
        }, status=201 if created else 200)

    def delete(self, request):
        """Remove a movie from favorites by TMDB ID."""
        tmdb_id = request.data.get('tmdb_id')
        favorite = FavoriteMovie.objects.filter(user=request.user, tmdb_id=tmdb_id).first()
        if favorite:
            favorite.delete()
            return Response({"message": "Removed from favorites"}, status=204)
        return Response({"error": "Not found"}, status=404)
