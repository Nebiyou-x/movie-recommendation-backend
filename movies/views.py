import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from .serializers import RegisterSerializer
from django.core.cache import cache
from rest_framework.permissions import IsAuthenticated
from .models import FavoriteMovie
from .serializers import FavoriteMovieSerializer

class TrendingMoviesView(APIView):
    def get(self, request):
        cache_key = "trending_movies"
        cached_data = cache.get(cache_key)

        if cached_data:
            return Response(cached_data)
        print("Fetching from TMDb")

        url = "https://api.themoviedb.org/3/trending/movie/week"
        params = { "api_key": settings.TMDB_API_KEY }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json().get('results', [])
            cache.set(cache_key, data, timeout=60 * 10)  # cache for 10 minutes
            return Response(data)
        except requests.RequestException:
            return Response({"error": "Failed to fetch trending movies"}, status=500)



    def get(self, request):
        url = f"https://api.themoviedb.org/3/trending/movie/week"
        params = {
            "api_key": settings.TMDB_API_KEY
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            return Response(data.get('results', []))
        except requests.RequestException:
            return Response({"error": "Failed to fetch trending movies"}, status=500)


class RecommendedMoviesView(APIView):
    def get(self, request):
        cache_key = "recommended_movies"
        cached_data = cache.get(cache_key)

        if cached_data:
            return Response(cached_data)
        print("Fetching from TMDb")

        url = "https://api.themoviedb.org/3/movie/top_rated"
        params = { "api_key": settings.TMDB_API_KEY }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json().get('results', [])[:10]
            cache.set(cache_key, data, timeout=60 * 10)  # 10 minutes
            return Response(data)
        except requests.RequestException:
            return Response({"error": "Failed to fetch recommended movies"}, status=500)

    def get(self, request):
        url = f"https://api.themoviedb.org/3/movie/top_rated"
        params = {
            "api_key": settings.TMDB_API_KEY
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            return Response(data.get('results', [])[:10])  # return top 10
        except requests.RequestException:
            return Response({"error": "Failed to fetch recommended movies"}, status=500)

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class FavoriteMovieView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        favorites = FavoriteMovie.objects.filter(user=request.user)
        serializer = FavoriteMovieSerializer(favorites, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = FavoriteMovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def delete(self, request):
        movie_id = request.data.get('movie_id')
        favorite = FavoriteMovie.objects.filter(user=request.user, movie_id=movie_id).first()
        if favorite:
            favorite.delete()
            return Response({"message": "Removed from favorites"}, status=204)
        return Response({"error": "Not found"}, status=404)
