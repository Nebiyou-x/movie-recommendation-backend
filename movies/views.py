import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings

class TrendingMoviesView(APIView):
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
