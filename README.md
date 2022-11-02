# OMDb_django
OMDb_django is an open source application to interact with OMDB API.
### Prerequisites:
- GIT (latest)
- Python ≥ 3.8
- Any code editor or IDE (PyCharm recommended for Python and Django)
- Any database client (optional)
## Installation

Go to  [OMDb API](http://www.omdbapi.com/apikey.aspx) to get an API Key

Clone the project

```bash
git clone https://github.com/abdoohossamm/OMDb_django.git
```

Change directory to the cloned project

```bash
cd OMDb_django
```

Make a copy of the example environment variables file and call it `.env`

```bash
cp .env.example .env
```

## Run the project

* Locally:

create a virtual environment
```bash
python -m venv venv
```
##### activating the virtual environment depends on the OS please serach for it

Install requirements packages after activating the virtual environment
```bash
pip install -r requirements.txt
```
migrate the model
```bash
python manage.py migrate
```

run django server
```bash
python manage.py runserver
```

## Search for the movie:
- go to this url: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- Search by Title or IMDB ID
