from unittest.mock import patch
from django.test import TestCase
from rest_framework import status
from movies import config
from movies.models import Movie, Comment
from movies.helpers import prepare_url
from movies.test_helpers.mock_sock import MockSockContext
from movies.test_helpers import mock_objects


class TestMoviesEndpoint(TestCase):

    def setUp(self):
        Movie.objects.create(**mock_objects.TEST_MOVIE_1)

    def test_create_new_movie(self):
        with MockSockContext(mock_objects.JSON_201) as ms:
            with patch('movies.helpers.prepare_url',
                       return_value="http://127.0.0.1") as prepare_url_function:
                url = prepare_url_function("http://127.0.0.1")
                data = {"title": "lord of the rings"}
                response = self.client.post('/movies/', data=data)
                self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_search_string_in_db(self):
        data = {"title": 'return of the'}
        response = self.client.post('/movies/', data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['Error'], config.RESOURCE_SHORT_EXISTS)

    def test_movie_in_db(self):
        with MockSockContext(mock_objects.JSON_400) as ms:
            with patch('movies.helpers.prepare_url',
                       return_value="http://127.0.0.1") as prepare_url_function:
                data = {"title": "return of the king"}
                response = self.client.post('/movies/', data=data)
                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
                self.assertEqual(response.json()['Error'], config.RESOURCE_FULL_EXISTS)

    def test_bad_request_params(self):
        data = {"tie": "return of the king"}
        response = self.client.post('/movies/', data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['Error'], config.REQUEST_BODY_ERROR_MOVIE)

    def test_movie_not_found(self):

        with MockSockContext(mock_objects.JSON_404) as ms:
            with patch('movies.helpers.prepare_url',
                       return_value="http://127.0.0.1") as prepare_url_function:
                url = prepare_url_function("http://127.0.0.1")
                data = {"title": "return 12345 asdfg"}
                response = self.client.post('/movies/', data=data)
                self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
                self.assertEqual(response.json()['Error'], config.MOVIE_NOT_FOUND)

    def test_get_movies(self):
        response = self.client.get('/movies/')

        movies = response.json()
        self.assertEqual(len(movies), 1)

        Movie.objects.create(**mock_objects.TEST_MOVIE_2)
        response = self.client.get('/movies/')

        movies = response.json()
        self.assertEqual(len(movies), 2)


class TestCommentsEndpoint(TestCase):

    def setUp(self):
        Movie.objects.create(**mock_objects.TEST_MOVIE_1)


    def test_create_comment(self):
        data = {"movieid": "1", "comment": "What a nice movie!"}
        response = self.client.post('/comments/', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_no_movie_in_db_not_found(self):
        data = {"movieid": "2", "comment": "What a nice movie!"}
        response = self.client.post('/comments/', data=data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json()['Error'], config.NO_MOVIE_ID)

    def test_bad_request_params__movieid(self):
        data = {"id": "2", "comment": "What a nice movie!"}
        response = self.client.post('/comments/', data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(config.REQUEST_BODY_ERROR_COMMENT_ID in response.json()['Error'].values())

    def test_bad_request_params_comment(self):
        data = {"movieid": "2", "comm": "What a nice movie!"}
        response = self.client.post('/comments/', data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(config.REQUEST_BODY_ERROR_COMMENT_COMMENT in response.json()['Error'].values())

    def test_bad_request_params_empty_comment(self):
        data = {"movieid": "2", "comment": ""}
        response = self.client.post('/comments/', data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(config.REQUEST_BODY_ERROR_COMMENT_EMPTY in response.json()['Error'].values())

    def test_bad_request_params_comment_too_short(self):
        data = {"movieid": "2", "comment": "abc"}
        response = self.client.post('/comments/', data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(config.REQUEST_BODY_ERROR_COMMENT_TOO_SHORT in response.json()['Error'].values())

    def test_get_comment_by_id(self):
        movie = Movie.objects.filter(id=1)
        Comment.objects.create(movieid=movie[0], comment="Absolutely shocking!")
        response = self.client.get('/comments/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_comments(self):

        movie = Movie.objects.filter(id=1)
        Comment.objects.create(movieid=movie[0], comment="Absolutely shocking!")
        Comment.objects.create(movieid=movie[0], comment="I wouldn't say so.")

        comments = Comment.objects.filter(movieid=1)

        response = self.client.get('/comments/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(comments.count(), 2)