from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from .models import Artist, Album, Track
from .serializers import ArtistSerializer, AlbumSerializer, TrackSerializer
from django.views.decorators.csrf import csrf_exempt
import base64

# Create your views here.

@csrf_exempt
def artist_list(request):
    if request.method == 'GET':
        artists = Artist.objects.all()
        serializer = ArtistSerializer(artists, many=True)
        return JsonResponse(serializer.data, safe=False)
    
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        try:
            byte_string = data['name'].encode('utf-8')
        except:
            return HttpResponse("input inválido",status=400)

        encoded_data = base64.b64encode(byte_string)
        encoded_data = encoded_data.decode('utf-8')
        coded = str(encoded_data[:22])
        data['artist_id'] = coded
        data['albums'] = '/artists/'+data['artist_id']+'/albums'
        data['tracks'] = '/artists/'+data['artist_id']+'/tracks'
        data['self_url'] = '/artists/'+data['artist_id']
        serializer = ArtistSerializer(data=data)

        if serializer.is_valid():
            try:
                artist = Artist.objects.get(artist_id=data['artist_id'])
                return JsonResponse(serializer.errors, status=409)
            except:
                serializer.save()
                return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
    else:
        return HttpResponse(status=405)

@csrf_exempt
def artist_detail(request, artist_id):
    try:
        artist = Artist.objects.get(artist_id=artist_id)

    except Artist.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = ArtistSerializer(artist)
        return JsonResponse(serializer.data)

    elif request.method == 'DELETE':
        artist.delete()
        return HttpResponse(status=204)

    else:
        return HttpResponse(status=405)

@csrf_exempt
def artist_albums(request, artist_id):
    
    if request.method == 'GET':
        try:
            artist = Artist.objects.get(artist_id=artist_id)

        except Artist.DoesNotExist:
            return HttpResponse(status=404)

        album = Album.objects.all().filter(artist='/artists/'+artist_id)
        serializer = AlbumSerializer(album, many=True)
        print(artist)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        try:
            artist = Artist.objects.get(artist_id=artist_id)

        except Artist.DoesNotExist:
            return HttpResponse(status=422)

        data = JSONParser().parse(request)
        data['artist'] = '/artists/'+artist_id

        try:
            string = data['name'] + ':' + data['artist']
        except:
            return HttpResponse("input inválido",status=400)
        
        byte_string = string.encode('utf-8')
        encoded_data = base64.b64encode(byte_string)
        encoded_data = encoded_data.decode('utf-8')
        coded = str(encoded_data[:22])
        data['album_id'] = coded
        data['tracks'] = '/albums/' + data['album_id'] + '/tracks'
        data['self_url'] = '/albums/' + data['album_id']
        serializer = AlbumSerializer(data=data)

        if serializer.is_valid():
            try:
                album = Album.objects.get(album_id=data['album_id'])
                return JsonResponse(serializer.errors, status=409)
            except:
                serializer.save(artist_link = artist)
                return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

    else:
        return HttpResponse(status=405)


@csrf_exempt
def artist_albums_play (request, artist_id):
    try: #Verifica que exista el artista
        artist = Artist.objects.get(artist_id=artist_id)

    except Artist.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'PUT':
        albums = Album.objects.all().filter(artist='/artists/'+artist_id)
        for album in albums:
            album_tracks_play(request, album.album_id)
        albums = Album.objects.all().filter(artist='/artists/'+artist_id)
        serializer = AlbumSerializer(albums, many=True)
        return JsonResponse(serializer.data, safe=False)

    else:
        return HttpResponse(status=405)

@csrf_exempt
def artist_tracks (request, artist_id):
    try:
        Artist.objects.get(artist_id=artist_id)

    except Artist.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        track = Track.objects.all().filter(artist='/artists/'+artist_id)
        serializer = TrackSerializer(track, many=True)
        return JsonResponse(serializer.data, safe=False)
    
    else:
        return HttpResponse(status=405)


@csrf_exempt
def album_list(request):
    if request.method == 'GET':
        albums = Album.objects.all()
        serializer = AlbumSerializer(albums, many=True)
        return JsonResponse(serializer.data, safe=False)
    
    else:
        return HttpResponse(status=405)

@csrf_exempt
def album_detail(request, album_id):
    try:
        album = Album.objects.get(album_id=album_id)

    except Album.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = AlbumSerializer(album)
        return JsonResponse(serializer.data)

    elif request.method == 'DELETE':
        album.delete()
        return HttpResponse(status=204)
    
    else:
        return HttpResponse(status=405)

@csrf_exempt
def album_tracks(request, album_id):
    
    if request.method == 'GET':
        try:
            album = Album.objects.get(album_id=album_id)

        except Album.DoesNotExist:
            return HttpResponse(status=404)

        track = Track.objects.all().filter(album='/albums/'+album_id)
        serializer = TrackSerializer(track, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        try:
            album = Album.objects.get(album_id=album_id)

        except Album.DoesNotExist:
            return HttpResponse(status=422)

        album_info = AlbumSerializer(album).data

        data = JSONParser().parse(request)
        data['album'] = '/albums/'+ album_id

        try:
            string = data['name'] + ':' + data['album']
        except:
            return HttpResponse("input inválido",status=400)
        
        byte_string = string.encode('utf-8')
        encoded_data = base64.b64encode(byte_string)
        encoded_data = encoded_data.decode('utf-8')
        coded = str(encoded_data[:22])
        data['track_id'] = coded
        data['times_played'] = 0
        data['artist'] = album_info['artist']
        data['self_url'] = '/tracks/' + data['track_id']
        serializer = TrackSerializer(data=data)

        if serializer.is_valid():
            try:
                track = Track.objects.get(track_id=data['track_id'])
                return JsonResponse(serializer.errors, status=409)
            except:
                serializer.save(album_link = album)
                return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

    else:
        return HttpResponse(status=405)


@csrf_exempt
def album_tracks_play(request, album_id):
    try: #Verifica que exista el álbum
        album = Album.objects.get(album_id=album_id)

    except Album.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'PUT':
        tracks = Track.objects.all().filter(album='/albums/'+album_id)
        for track in tracks:
            track_detail_play(request, track.track_id)
        tracks = Track.objects.all().filter(album='/albums/'+album_id)
        serializer = TrackSerializer(tracks, many=True)
        return JsonResponse(serializer.data, safe=False)
    
    else:
        return HttpResponse(status=405)


@csrf_exempt
def track_list(request):
    if request.method == 'GET':
        tracks = Track.objects.all()
        serializer = TrackSerializer(tracks, many=True)
        return JsonResponse(serializer.data, safe=False)
    
    else:
        return HttpResponse(status=405)


@csrf_exempt
def track_detail(request, track_id):
    try:
        track = Track.objects.get(track_id=track_id)

    except Track.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = TrackSerializer(track)
        return JsonResponse(serializer.data)

    elif request.method == 'DELETE':
        track.delete()
        return HttpResponse(status=204)
    
    else:
        return HttpResponse(status=405)

@csrf_exempt
def track_detail_play(request, track_id):
    try:
        track = Track.objects.get(track_id=track_id)

    except Track.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'PUT':
        track_info = TrackSerializer(track).data
        data = dict()
        data['track_id'] = track_info['track_id']
        data['name'] = track_info['name']
        data['duration'] = track_info['duration']
        data['times_played'] = track_info['times_played'] + 1
        data['artist'] = track_info['artist']
        data['album'] = track_info['album']
        data['self_url'] = track_info['self_url']

        serializer = TrackSerializer(track, data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=200)
        return JsonResponse(serializer.errors, status=400) #Nunca debería mostrar este error

    else:
        return HttpResponse(status=405)