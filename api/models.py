from django.db import models
from django.core.validators import RegexValidator

# Create your models here.

class Artist(models.Model):
    artist_id = models.CharField(max_length=22)
    name = models.CharField(max_length=200)
    age = models.IntegerField()
    albums = models.CharField(max_length=200)
    tracks = models.CharField(max_length=200)
    self_url = models.CharField(max_length=200)
    
    def __str__(self):
        return self.artist_id

class Album(models.Model):
    album_id = models.CharField(max_length=22)
    name = models.CharField(max_length=200)
    genre = models.CharField(max_length=200)
    artist = models.CharField(max_length=200)
    artist_link = models.ForeignKey('Artist', on_delete=models.CASCADE, null=True)
    tracks = models.CharField(max_length=200)
    self_url = models.CharField(max_length=200)
    
    def __str__(self):
        return self.album_id

class Track(models.Model):
    track_id = models.CharField(max_length=22)
    name = models.CharField(max_length=200)
    duration = models.FloatField()
    times_played = models.IntegerField()
    artist = models.CharField(max_length=200)
    album = models.CharField(max_length=200)
    album_link = models.ForeignKey('Album', on_delete=models.CASCADE, null=True)
    self_url = models.CharField(max_length=200)
    
    def __str__(self):
        return self.track_id
