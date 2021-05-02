from rest_framework import serializers
from .models import Artist, Album, Track


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ['artist_id', 'name', 'age', 'albums', 'tracks', 'self_url']

class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = ['album_id', 'name', 'genre', 'artist', 'tracks', 'self_url']

class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = ['track_id', 'name', 'duration', 'times_played', 'artist', 'album', 'self_url']
