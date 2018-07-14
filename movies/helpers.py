import urllib
import requests
from rest_framework.response import Response
from .models import Movie, Comment
from movies import config


def check_title_short_in_db(movie_title):
    return Movie.objects.filter(searchstring=movie_title)


def check_title_full_in_db(full_movie_title):
    return Movie.objects.filter(title=full_movie_title)


def check_movie_id_in_db(movie_id):
    return Movie.objects.filter(id=movie_id)


def prepare_url(movie_title):
    api_url = 'http://www.omdbapi.com/?'
    api_url_params = {"t": movie_title, "apikey": config.APIKEY}
    url = (api_url + urllib.parse.urlencode(api_url_params))
    return url


def make_omdbapi_request(movie_title):
    url = prepare_url(movie_title)
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.Timeout:
        response = Response()
        response.status_code = 408

    return response


def handle_omdbapi_response(movie_title, response):

    if response.status_code == 200:

        movie_json = response.json()
        if "Error" in movie_json:
            return Response({"Error": config.MOVIE_NOT_FOUND}, status=404)

        full_title = movie_json['Title']
        if check_title_full_in_db(full_title):
            return Response({"Error" : config.RESOURCE_FULL_EXISTS}, status=400)

        movie_json = validate_omdbapi_response_against_movie_model(movie_json)
        movie_json['searchstring'] = movie_title
        create_movie_entry(movie_json)
        return Response(movie_json, status=201)

    else:
        return Response(response.content, status=response.status_code)


def validate_omdbapi_response_against_movie_model(omdbapi_response_json):

    validated_json = {}
    json_to_lowercase = dict((k.lower(), v) for k, v in omdbapi_response_json.items())

    for key in json_to_lowercase:
        if hasattr(Movie, key):
           validated_json[key] = json_to_lowercase.get(key)

    return validated_json


def create_movie_entry(movie_json):
    Movie.objects.create(**movie_json)


def create_comment_entry(comment_json):
    Comment.objects.create(**comment_json)


def validate_comment_request_body(request):
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

