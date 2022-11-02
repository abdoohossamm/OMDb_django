import re
from django.shortcuts import render, redirect, reverse
from movies.forms import SearchTitleForm, SearchImdbForm
from movies.models import Movie
from movies.omdb_integration import search_and_save, fill_movie_details
from django.views import View


class Index(View):
    ctx = {
        'title_form': SearchTitleForm(),
        'imdb_form': SearchImdbForm(),
    }

    def get(self, request):
        return render(request, 'movies/index.html', self.ctx)

    def post(self, request):
        title = request.POST.get('title', False)
        imdb_id = request.POST.get('imdb_id')
        if title:
            return redirect(reverse('search_title', kwargs={'title': title}))
        if imdb_id:
            return redirect(reverse('search_imdb', kwargs={'imdb': imdb_id}))


def search_title(request, title):
    search_str = re.sub(r"\s+", " ", title.lower()).strip()

    search_and_save(search_str)

    movies = Movie.objects.filter(title__icontains=search_str)

    ctx = {
        'movies': movies,
        'search': search_str,
    }
    return render(request, 'movies/movie_table.html', ctx)


def search_imdb(request, imdb):
    search_str = re.sub(r"\s+", " ", imdb.lower()).strip()
    movie = Movie.objects.get(imdb_id=search_str)
    fill_movie_details(movie)

    ctx = {
        'movie': movie,
        'search': imdb,
    }
    return render(request, 'movies/movie_detail.html', ctx)
