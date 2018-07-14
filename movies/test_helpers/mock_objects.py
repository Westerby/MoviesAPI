TEST_MOVIE_1 = {'actors': 'Brad Stapleton, Jeff Weinkam',
         'awards': 'N/A',
         'boxoffice': 'N/A',
         'country': 'USA',
         'director': 'Tyler Meyer',
         'dvd': 'N/A',
         'genre': 'N/A',
         'imdbid': 'tt2125599',
         'imdbrating': 'N/A',
         'imdbvotes': 'N/A',
         'language': 'English',
         'metascore': 'N/A',
         'plot': 'N/A',
         'poster': 'N/A',
         'production': 'N/A',
         'rated': 'N/A',
         'released': '28 Apr 2006',
         'runtime': '95 min',
         'searchstring': 'return of the',
         'title': 'Return of the King',
         'type': 'movie',
         'website': 'N/A',
         'writer': 'Jeff Weinkam',
         'year': 2006}

TEST_MOVIE_2 = {'actors': 'Miroslaw Hermaszewski',
        'awards': 'N/A',
        'boxoffice': 'N/A',
        'country': 'N/A',
        'director': 'Bohdan Swiatkiewicz',
        'dvd': 'N/A',
        'genre': 'Documentary, Biography',
        'imdbid': 'tt2013246',
        'imdbrating': 'N/A',
        'imdbvotes': 'N/A',
        'language': 'N/A',
        'metascore': 'N/A',
        'plot': 'N/A',
        'poster': 'N/A',
        'production': 'N/A',
        'rated': 'N/A',
        'released': 'N/A',
        'runtime': 'N/A',
        'searchstring': 'miroslaw',
        'title': 'Miroslaw Hermaszewski',
        'type': 'movie',
        'website': 'N/A',
        'writer': 'Bohdan Swiatkiewicz, Bohdan Swiatkiewicz',
        'year': 1978}

JSON_404 = b"""\
        HTTP/1.1 200 OK
        Content-Type: application/json
        Content-length: 20

        {"Error" : "Movie not found"}""".replace(b"\n", b"\r\n")

JSON_400 = b"""\
        HTTP/1.1 200 OK
        Content-Type: application/json
        Content-length: 545

        {"Actors": "Brad Stapleton, Jeff Weinkam",
         "Awards": "N/A",
         "BoxOffice": "N/A",
         "Country": "USA",
         "DVD": "N/A",
         "Director": "Tyler Meyer",
         "Genre": "N/A",
         "Language": "English",
         "Metascore": "N/A",
         "Plot": "N/A",
         "Poster": "N/A",
         "Production": "N/A",
         "Rated": "N/A",
         "Ratings": [],
         "Released": "28 Apr 2006",
         "Response": "True",
         "Runtime": "95 min",
         "Title": "Return of the King",
         "Type": "movie",
         "Website": "N/A",
         "Writer": "Jeff Weinkam",
         "Year": "2006",
         "imdbID": "tt2125599",
         "imdbRating": "N/A",
         "imdbVotes": "N/A"}""".replace(b"\n", b"\r\n")

JSON_201 = b"""\
        HTTP/1.1 200 OK
        Content-Type: application/json
        Content-length: 1494

        {"Actors": "Noel Appleby, Ali Astin, Sean Astin, David Aston",
         "Awards": "Won 11 Oscars. Another 197 wins & 122 nominations.",
         "BoxOffice": "$364,000,000",
         "Country": "USA, New Zealand",
         "DVD": "25 May 2004",
         "Director": "Peter Jackson",
         "Genre": "Adventure, Drama, Fantasy",
         "Language": "English, Quenya, Old English, Sindarin",
         "Metascore": "94",
         "Plot": "Gandalf and Aragorn lead the World of Men against Saurons army to draw his gaze from Frodo and Sam as they approach Mount Doom with the One Ring.",
         "Poster": "https://m.media-amazon.com/images/M/MV5BNzA5ZDNlZWMtM2NhNS00NDJjLTk4NDItYTRmY2EwMWZlMTY3XkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_SX300.jpg",
         "Production": "New Line Cinema",
         "Rated": "PG-13",
         "Ratings": [{"Source": "Internet Movie Database", "Value": "8.9/10"},
          {"Source": "Rotten Tomatoes", "Value": "93%"},
          {"Source": "Metacritic", "Value": "94/100"}],
         "Released": "17 Dec 2003",
         "Response": "True",
         "Runtime": "201 min",
         "Title": "The Lord of the Rings: The Return of the King",
         "Type": "movie",
         "Website": "http://www.lordoftherings.net/",
         "Writer": "J.R.R. Tolkien (novel), Fran Walsh (screenplay), Philippa Boyens (screenplay), Peter Jackson (screenplay)",
         "Year": "2003",
         "imdbID": "tt0167260",
         "imdbRating": "8.9",
         "imdbVotes": "1,401,555"}""".replace(b"\n", b"\r\n")
