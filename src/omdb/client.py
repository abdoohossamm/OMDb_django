import logging
from typing import (Dict, AnyStr, List, Optional)
import requests

logger = logging.getLogger(__name__)

OMDB_API_URL = "https://www.omdbapi.com/"


class OmdbMovie:
    """
    A simple class to represent movie data coming back from OMDb and transform to Python types.
    """

    def __init__(self, data: Dict):
        """Data is the raw JSON/dict returned from OMDb"""
        assert isinstance(data, Dict), f'Excepted Dictionary/Json but got {type(data)}'
        self.data = data

    def check_for_detail_data_key(self, key):
        """
        Some keys are only in the detail response,
        raise an exception if the key is not found.
        """

        if key not in self.data:
            raise AttributeError(
                f"{key} is not in data, please make sure this is a detail response."
            )
        if self.data[key].lower() == "n/a":
            self.data[key] = None
    @property
    def imdb_id(self) -> AnyStr:
        return self.data["imdbID"]

    @property
    def title(self) -> AnyStr:
        return self.data["Title"]

    @property
    def year(self) -> int:
        return int(self.data["Year"])

    @property
    def runtime_minutes(self):
        self.check_for_detail_data_key("Runtime")

        if self.data["Runtime"] is None:
            return None

        rt, units = self.data["Runtime"].split(" ")

        if units != "min":
            raise ValueError(f"Expected units 'min' for runtime. Got '{units}")

        return int(rt)

    @property
    def genres(self) -> List:
        self.check_for_detail_data_key("Genre")

        return self.data["Genre"].split(", ")

    @property
    def plot(self) -> AnyStr:
        self.check_for_detail_data_key("Plot")
        return self.data["Plot"]


class OmdbClient:

    def __init__(self, api_key):
        self.api_key = api_key

    def make_request(self, params: Dict) -> requests.Response:
        """
        Make GET request to the API,
        automatically adding the `apikey` to parameters
        """
        assert isinstance(params, Dict), f'Excepted Dictionary/Json but got {type(params)}'
        params['apikey'] = self.api_key

        resp = requests.get(OMDB_API_URL, params=params)
        resp.raise_for_status()
        return resp

    def get_by_imdb_id(self, imdb_id: AnyStr) -> OmdbMovie:
        """
        Get a movie by its IMDB ID
        int: imdb_id
        """
        assert isinstance(imdb_id, str), f'Excepted Text/String but got {type(imdb_id)}'
        logger.info(f'fetching detail for IMDB ID {imdb_id}')
        resp = self.make_request({'i': imdb_id})
        return OmdbMovie(resp.json())

    def search(self, search: AnyStr) -> OmdbMovie:
        """
        @Generator
        Search for movies by title.
        This is a generator so all results from all pages will be iterated across.
        """
        assert isinstance(search, str), f'Excepted Text/String but got {type(search)}'
        page = 1
        seen_results = 0
        total_results = None

        logger.info(f"Perfoming a search for {search}")

        while True:
            logger.info(f"Fetching page {page}")
            resp = self.make_request({"s": search, "type": "movie", "page": str(page)})
            resp_body = resp.json()
            if total_results is None:
                total_results = int(resp_body['totalResults'])
            for movie in resp_body['Search']:
                seen_results += 1
                yield OmdbMovie(movie)
            if seen_results >= total_results:
                break
            page += 1
