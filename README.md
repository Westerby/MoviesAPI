# Movies API

Movies API is a simple REST API that enables user to create new resources
- movies and comments about those movies, as well as retrieving
information about movies and comments.

## Using API

#### POST /movies
Creates new Movie object based on POST request body parameter: "title".
Example:
`requests.post({hostname}/movies/, data={'title': 'return of the king'}`

#### GET /movies
Returns a json with all Movies existing in the database.
Example:
`requests.get({hostname}/movies/)`

#### POST /comments
Creates new Comment object based on POST request parameters: "movieid"
and "comment". Creation of new comments is possible only for existing
movies.
`requests.post('{hostname}/comments/', data={"movieid": "1", "comment": "Great movie!"})`

#### GET /comments
Returns a json with all Comments existing in the database.
`requests.get('{hostname}/comments/')`

#### GET /comments/<movieid>
Request url can be parametrized to filter comments by movie id.
`request.get('{hostname}/comments/{movieid}/')`

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