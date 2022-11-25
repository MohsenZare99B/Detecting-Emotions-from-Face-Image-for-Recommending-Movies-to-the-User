from email.policy import default
from operator import mod
from django.db import models
import uuid
# Create your models here.

class Movie(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False,
    primary_key=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(null=True, blank=True, default="default_movie.png")

    def __str__(self):
        return self.title

class Users(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False,
    primary_key=True)
    username = models.CharField(max_length=200, unique=True)
    password = models.CharField(max_length=200)

class Vote(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False,
    primary_key=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    romance = models.IntegerField()
    horror = models.IntegerField()
    comedy = models.IntegerField()
    action = models.IntegerField()
    fantasy = models.IntegerField()
    username = models.CharField(max_length=200)

    def __str__(self):
        return self.movie.title + " | " + self.username

class Movie_feature(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False,
    primary_key=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    romance = models.IntegerField()
    horror = models.IntegerField()
    comedy = models.IntegerField()
    action = models.IntegerField()
    fantasy = models.IntegerField()
    no_of_votes = models.IntegerField()

    def __str__(self):
        return self.movie.title

class Romance_pic(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False,
    primary_key=True)
    image = models.ImageField(null=True, blank=True, default="default_movie.png")

class Horror_pic(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False,
    primary_key=True)
    image = models.ImageField(null=True, blank=True, default="default_movie.png")

class Comedy_pic(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False,
    primary_key=True)
    image = models.ImageField(null=True, blank=True, default="default_movie.png")

class Action_pic(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False,
    primary_key=True)
    image = models.ImageField(null=True, blank=True, default="default_movie.png")

class Fantasy_pic(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False,
    primary_key=True)
    image = models.ImageField(null=True, blank=True, default="default_movie.png")

class Emotional_state_feature(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False,
    primary_key=True)
    emotional_state = models.CharField(max_length=7)
    romance = models.IntegerField()
    horror = models.IntegerField()
    comedy = models.IntegerField()
    action = models.IntegerField()
    fantasy = models.IntegerField()
    no_of_votes = models.IntegerField()


class Comment(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False,
    primary_key=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    text = models.CharField(max_length=800)
    date = models.DateTimeField(auto_now_add=True)
    username = models.CharField(max_length=200)

    def __str__(self):
        return self.movie.title + " | " + self.username