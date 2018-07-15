import urllib
import requests
from rest_framework.response import Response
from .models import Movie, Comment, Rating
from .serializers import RatingSerializer, MovieSerializer
from movies import config


def prepare_movies_get_response():
    """Prepares response body with all movies and ratings.
    :return (list) list of dics, every dict contains movie information
    """
    response = []
    movies = Movie.objects.all()
    for movie in movies:
        movie_serializer = MovieSerializer(movie)
        ratings = Rating.objects.filter(movieid=movie.id)
        movie = dict(movie_serializer.data)
        if ratings:
            ratings_serializer = RatingSerializer(ratings, many=True)
            ratings = [dict(x) for x in ratings_serializer.data]
            movie['ratings'] = ratings

        response.append(movie)
    return response


def check_title_short_in_db(movie_title):
    """Checks if POST parameter - movie title - has already been used
    and exists in database.
    :param movie_title:
    :return: django Queryset of Movie objects
    """
    return Movie.objects.filter(searchstring=movie_title)


def check_title_full_in_db(full_movie_title):
    """Checks if movie with given full title exists in database.
    :param full_movie_title:
    :return: django Queryset of Movie objects
    """
    return Movie.objects.filter(title=full_movie_title)


def check_movie_id_in_db(movie_id):
    """Checks if movie with given ID exists in database.
    :param movie_id:
    :return: django Queryset of Movie objects
    """
    return Movie.objects.filter(id=movie_id)


def prepare_url(movie_title):
    """Prepares parametrized URL to OMDBAPI.
    :param (str) movie_title:
    :return: (str) url
    """
    api_url = 'http://www.omdbapi.com/?'
    api_url_params = {"t": movie_title, "apikey": config.APIKEY}
    url = (api_url + urllib.parse.urlencode(api_url_params))
    return url


def make_omdbapi_request(movie_title):
    """Performs GET request to OMDBAPI.
    :param (str) movie_title
    :return: (requests.models.Response) request
    """
    url = prepare_url(movie_title)
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.Timeout:
        response = Response()
        response.status_code = 408

    return response


def handle_omdbapi_response(movie_title, response):
    """Performs checks on OMBDAPI response object. If objects json file is valid
    new Movie object is created and written to the database.
    :param (str) movie_title
    :param (requests.models.Response) request
    :return: rest_framework Response object
    """
    if response.status_code == 200:

        movie_json = response.json()
        if "Error" in movie_json:
            return Response({"Error": config.MOVIE_NOT_FOUND}, status=404)
        try:
            full_title = movie_json['Title']
            if check_title_full_in_db(full_title):
                return Response({"Error": config.RESOURCE_FULL_EXISTS}, status=400)
        except KeyError as ex:
            return Response({"Error": config.NO_TITLE_IN_RESPONSE}, status=404)

        valid_movie_json = validate_omdbapi_response_against_movie_model(movie_json)
        valid_movie_json['searchstring'] = movie_title

        movie = create_movie_entry(valid_movie_json)

        try:
            ratings = movie_json['Ratings']
            if ratings:
                ratings = create_rating_entries(movie, ratings)
                valid_movie_json['ratings'] = ratings
        except KeyError as ex:
            print("No ratings field for {}".format(full_title))

        return Response(valid_movie_json, status=201)

    else:
        return Response(response.content, status=response.status_code)


def validate_omdbapi_response_against_movie_model(omdbapi_response_json):
    """Checks that json file to be written to database consist only of Model fields.
    :param (dict) omdbapi_response_json:
    :return: (dict) validated json
    """
    validated_json = {}
    json_to_lowercase = dict((k.lower(), v) for k, v in omdbapi_response_json.items())

    for key in json_to_lowercase:
        if hasattr(Movie, key):
            validated_json[key] = json_to_lowercase.get(key)

    return validated_json


def create_movie_entry(movie_json):
    """Writes a Movie object to database.
    :param (dict) movie_json:
    :return: Movie object
    """
    return Movie.objects.create(**movie_json)


def create_comment_entry(comment_json):
    """Writes a Comment object do database.
    :param (dict)comment_json:
    :return: Comment object
    """
    return Comment.objects.create(**comment_json)


def create_rating_entries(movie, ratings):
    """Writes Rating objects to database
    :param Movie object:
    :param (dict) ratings
    :return: (dict) processed ratings
    """
    for rating in ratings:
        Rating.objects.create(movieid=movie, source=rating['Source'],
                              rating=rating['Value'])

    ratings = Rating.objects.filter(movieid=movie.id)
    serializer = RatingSerializer(ratings, many=True)
    return [dict(x) for x in serializer.data]


def validate_comment_request_body(request):
    """Validates body of POST request which creates new comment object.
    :param requests Request object:
    :return: (dict) response
    """
    response = {}

    try:
        request.data['movieid']
    except KeyError:
        response["movieid"] = config.REQUEST_BODY_ERROR_COMMENT_ID
    try:
        comment = request.data['comment']
        if not comment:
            response["comment"] = config.REQUEST_BODY_ERROR_COMMENT_EMPTY
        elif len(comment) < 6:
            response["comment"] = config.REQUEST_BODY_ERROR_COMMENT_TOO_SHORT
    except KeyError:
        response["comment"] = config.REQUEST_BODY_ERROR_COMMENT_COMMENT

    return response
