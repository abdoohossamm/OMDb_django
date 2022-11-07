"""
Controller for movies app
"""
import re
import urllib.parse
from celery.exceptions import TimeoutError

from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views import View

from src.celery import app

from movies.forms import SearchTitleForm, SearchImdbForm
from movies.models import Movie
from movies.omdb_integration import search_and_save, fill_movie_details
from movies.tasks import search_and_save as search_and_save_task


class Index(View):
    """
    The home page that can receive post and get request.
    GET request shows the home page.
    POST request redirect the user to search result page.
    """
    ctx = {
        'title_form': SearchTitleForm(),
        'imdb_form': SearchImdbForm(),
    }

    def get(self, request):
        """
        GET request shows the home page.
        """
        return render(request, 'movies/index.html', self.ctx)

    def post(self, request):
        """
        POST request redirect the user to search result page.
        """
        title = request.POST.get('title', False)
        imdb_id = request.POST.get('imdb_id')
        if title:
            return redirect(reverse('search_title', kwargs={'title': title}))
        if imdb_id:
            return redirect(reverse('search_imdb', kwargs={'imdb': imdb_id}))


def search_title(request, title):
    """
    Search page for Title
    """
    # remove the more than one space and strip from both sides
    search_str = re.sub(r"\s+", " ", title.lower()).strip()

    search_and_save(search_str)

    movies = Movie.objects.filter(title__icontains=search_str)

    ctx = {
        'movies': movies,
        'search': search_str,
    }
    return render(request, 'movies/movie_table.html', ctx)


def search_imdb(request, imdb):
    """
    Search page for IMDB
    """

    # remove the more than one space and strip from both sides
    search_str = re.sub(r"\s+", " ", imdb.lower()).strip()

    movie = get_object_or_404(Movie, imdb_id=search_str)
    fill_movie_details(movie)

    ctx = {
        'movie': movie,
        'search': imdb,
    }
    return render(request, 'movies/movie_detail.html', ctx)


def _404_not_found(request, exception):
    """
    404 NOT FOUND page.
    """
    return render(request, '404.html')


def search(request):
    search_term = request.GET['search_term']
    res = search_and_save_task.delay(search_term)
    try:
        res.get(timeout=2)
    except TimeoutError:
        return redirect(
            reverse("search_wait", args=(res.id,))
            + "?search_term="
            + urllib.parse.quote_plus(search_term)
        )
    return redirect(
        reverse("search_results")
        + "?search_term="
        + urllib.parse.quote_plus(search_term),
        permanent=False,
    )


def search_wait(request, result_uuid):
    search_term = request.GET["search_term"]
    res = app.AsyncResult(result_uuid)

    try:
        res.get(timeout=-1)
    except TimeoutError:
        return HttpResponse("Task pending, please refresh.", status=200)

    return redirect(
        reverse("search_results")
        + "?search_term="
        + urllib.parse.quote_plus(search_term)
    )


def search_results(request):
    search_term = request.GET["search_term"]
    movies = Movie.objects.filter(title__icontains=search_term)
    return HttpResponse(
        "\n".join([movie.title for movie in movies]), content_type="text/plain"
    )
