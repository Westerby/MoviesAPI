from rest_framework.views import  APIView
from rest_framework.response import Response
from .models import Movie, Comment
from .serializers import MovieSerializer, CommentSerializer
from movies import helpers
from movies import config

class MovieEndpoint(APIView):

    def get(self, request):
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)

    def post(self, request):
        try:
            movie_title_from_post = request.data['title']
        except KeyError:
            return Response({"Error": config.REQUEST_BODY_ERROR_MOVIE}, status=400)

        title_short_in_db = helpers.check_title_short_in_db(movie_title_from_post)

        if title_short_in_db:
            return Response({"Error": config.RESOURCE_SHORT_EXISTS}, status=400)

        omdbapi_response = helpers.make_omdbapi_request(movie_title_from_post)
        response = helpers.handle_omdbapi_response(movie_title_from_post, omdbapi_response)
        return response

class CommentsEndpoint(APIView):

    def get(self, request, id=0):
        if not id:
            comments = Comment.objects.all()
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data)

        comments = Comment.objects.filter(movieid=id)
        if not comments:
            return Response({"Error" : config.NO_COMMENTS}, status=404)

        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request):

        not_valid = helpers.validate_comment_request_body(request)
        if not_valid:
            return Response({"Error" : not_valid}, status=400)

        comment_json = request.data.dict()
        movieid = comment_json['movieid']
        comment = comment_json['comment']
        movie = helpers.check_movie_id_in_db(movieid)

        if not movie:
            return Response({"Error" : config.NO_MOVIE_ID}, status=404)

        Comment.objects.create(movieid=movie[0], comment=comment)
        return Response(comment_json, status=201)

