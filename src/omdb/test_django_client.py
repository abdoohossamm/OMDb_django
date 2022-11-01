from django.test import TestCase
from django.conf import settings
from src.omdb.client import OmdbMovie, OmdbClient, OMDB_API_URL


class TestOmdbMovie(TestCase):
    def setUp(self) -> None:
        self.data = {
            'imdbID': '1253',
            'Title': 'My movie',
            'Year': '1991',
            'Runtime': '90 min',
            'Genre': 'Action, Comedy'
        }

    def test_omdb_result(self):
        movie = OmdbMovie(self.data)
        # Check the class itself
        self.assertRaises(AssertionError, OmdbMovie, ['Title', 'Year'])
        # test movie.check_for_detail_data_key() method
        self.assertRaises(AttributeError, movie.check_for_detail_data_key, 'unknown')
        # check for properties
        self.assertEqual(movie.imdb_id, self.data['imdbID'])
        self.assertEqual(movie.title, self.data['Title'])
        self.assertEqual(movie.year, int(self.data['Year']))
        self.assertEqual(movie.runtime_minutes, int(self.data['Runtime'].split(' ')[0]))
        self.assertEqual(movie.genres, self.data['Genre'].split(', '))
        with self.assertRaises(AttributeError) as e:
            movie.plot

    def test_omdb_properties(self):
        data2 = {
            'imdbID': '12',
            'Title': 'movie',
            'Year': '1991',
            'Runtime': '90 sec',
            'Plot': 'Plot'
        }
        movie = OmdbMovie(data2)

        # check for properties
        self.assertEqual(movie.imdb_id, data2['imdbID'])
        self.assertEqual(movie.title, data2['Title'])
        self.assertEqual(movie.year, int(data2['Year']))
        self.assertEqual(movie.plot, data2['Plot'])
        with self.assertRaises(AttributeError) as e:
            movie.genres
        with self.assertRaises(ValueError) as e:
            movie.runtime_minutes


class TestOmdbClient(TestCase):
    def setUp(self) -> None:
        self.data = {
            'imdbID': '1253',
            'Title': 'My movie',
            'Year': '1991',
            'Runtime': '90 min',
            'Genre': 'Action, Comedy'
        }
        self.api_key = settings.OMDB_KEY
        self.client = OmdbClient(self.api_key)

    def test_make_request(self):
        params = {}
        resp = self.client.make_request(params=params)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.headers['Content-Type'], 'application/json; charset=utf-8')

    def test_get_by_imdb_id(self):
        # imdb for django unchained movie
        imdb_id = 'tt1853728'
        movie = self.client.get_by_imdb_id(imdb_id)
        self.assertEqual(movie.title, "Django Unchained")
        self.assertEqual(movie.year, 2012)
        self.assertEqual(movie.runtime_minutes, 165)

    def test_search(self):
        # imdb for django unchained movie
        search = 'django'
        movies = self.client.search
        for movie in movies(search):
            self.assertIsInstance(movie, OmdbMovie)
            self.assertEqual(movie.title.lower().find(search) != -1, True)
