APIKEY = 'a874098f'

RESOURCE_SHORT_EXISTS = """Could not create resource. Resource with requested movie
title already exist. You can try full movie title if the
movie does not appear in the results.""".replace('\n',' ')

RESOURCE_FULL_EXISTS = """Could not create resource. Resource with requested movie
title already exist.""".replace('\n',' ')

REQUEST_BODY_ERROR_MOVIE = """There is an error in your request body. Body should
contain "title" field.
""".replace('\n',' ')

REQUEST_BODY_ERROR_COMMENT_ID = """There is an error in your request body. Body should
contain "movieid" field.
""".replace('\n',' ')

REQUEST_BODY_ERROR_COMMENT_COMMENT = """There is an error in your request body. Body
should contain "comment" field.
""".replace('\n',' ')

REQUEST_BODY_ERROR_COMMENT_EMPTY = """Comment cannot be empty.
""".replace('\n',' ')

REQUEST_BODY_ERROR_COMMENT_TOO_SHORT = """Comment has to be longer than 5 characters.
""".replace('\n',' ')

NO_COMMENTS = """There are no comments for requested movie id.
""".replace('\n',' ')

NO_MOVIE_ID = """There is no movie for requested movie id.
""".replace('\n',' ')

MOVIE_NOT_FOUND = """Movie not found.""".replace('\n',' ')

