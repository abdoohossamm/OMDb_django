from django.db import models


class SearchTerm(models.Model):
    class Meta:
        ordering = ["id"]

    term = models.TextField(unique=True)
    last_search = models.DateTimeField(auto_now=True)


class Genre(models.Model):
    class Meta:
        ordering = ["name"]

    name = models.TextField(unique=True)


class Movie(models.Model):
    class Meta:
        ordering = ["title", "year"]

    title = models.TextField()
    year = models.PositiveIntegerField()
    runtime_minutes = models.PositiveIntegerField(null=True)
    imdb_id = models.SlugField(unique=True)
    genres = models.ManyToManyField(Genre, related_name="movies")
    plot = models.TextField(null=True, blank=True)
    is_full_record = models.BooleanField(default=False)