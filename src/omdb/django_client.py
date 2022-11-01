from django.conf import settings

from src.omdb.client import OmdbClient


def get_client_from_settings():
    """Create an instance of an OmdbClient using the OMDB_KEY from the Django settings."""
    return OmdbClient(settings.OMDB_KEY)
