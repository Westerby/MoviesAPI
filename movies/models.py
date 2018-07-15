from django.db import models

class Movie(models.Model):
    id = models.AutoField(primary_key=True)
    searchstring = models.CharField(max_length=200, default="a movie title")
    title = models.CharField(max_length=1000)
    year = models.IntegerField()
    rated = models.CharField(max_length=20)
    released = models.CharField(max_length=14)
    runtime = models.CharField(max_length=9)
    genre = models.CharField(max_length=100)
    director = models.CharField(max_length=100)
    writer = models.CharField(max_length=9)
    actors = models.CharField(max_length=200)
    plot = models.TextField()
    language = models.CharField(max_length=100)
    country = models.CharField(max_length=50)
    awards = models.CharField(max_length=100)
    poster = models.CharField(max_length=200)
    metascore = models.CharField(max_length=10)
    imdbrating = models.CharField(max_length=10)
    imdbvotes = models.CharField(max_length=20)
    imdbid = models.CharField(max_length=20)
    type = models.CharField(max_length=20)
    dvd = models.CharField(max_length=20)
    boxoffice = models.CharField(max_length=20)
    production = models.CharField(max_length=20)
    website = models.CharField(max_length=20)

class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    movieid = models.ForeignKey(Movie, on_delete=models.CASCADE)
    comment = models.TextField()

class Rating(models.Model):
    id = models.AutoField(primary_key=True)
    movieid = models.ForeignKey(Movie, on_delete=models.CASCADE)
    source = models.CharField(max_length=100)
    rating = models.CharField(max_length=20)