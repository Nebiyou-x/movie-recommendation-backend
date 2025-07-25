from django.db import models
from django.contrib.auth.models import User

class FavoriteMovie(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    movie_id = models.IntegerField()
    title = models.CharField(max_length=255)
    poster_path = models.URLField(blank=True, null=True)

    class Meta:
        unique_together = ('user', 'movie_id')

    def __str__(self):
        return f"{self.user.username} - {self.title}"
