# Movies API

Movies API is a simple REST API that enables user to create new resources - movies and comments about those movies, as well as retrieving information about movies and comments.

## Using API

### POST /movies

### GET /movies

### POST /comments

### GET /comments

### GET /comments/<movieid>

## Deployment

1. Create and activate new python environment
```
$ python -m venv moviesapi
$ cd moviesapi
$ Scripts/activate.bat
```
2. Clone repository.
`$ git clone https://github.com/Westerby/MoviesAPI.git`

3. Install requirements.
`$ pip install -r requirements.txt`

4. Run tests to check if everything is all right.
`$ python manage.py test movies.tests`

5. Run server.
`$ python manage.py runserver`