from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from .models import Artist, Album, Track
from .serializers import ArtistSerializer, AlbumSerializer, TrackSerializer
from django.views.decorators.csrf import csrf_exempt
import base64

# Create your views here.

def data_show(variable):
    dicionario = dict()
    lista = []
    
    for dic in variable:
        for key, value in dic.items():
            if "_id" in key:
                dicionario["id"] = value
            elif "self_" in key:
                dicionario["self"] = value
            else:
                dicionario[key] = value
        lista.append(dicionario)
    return lista


def data_show_unit(variable):
    dicionario = dict()
    
    for key, value in variable.items():
        if "_id" in key:
            dicionario["id"] = value
        elif "self_" in key:
            dicionario["self"] = value
        else:
            dicionario[key] = value
    return dicionario


@csrf_exempt
def artist_list(request):
    if request.method == 'GET':
        artists = Artist.objects.all()
        serializer = ArtistSerializer(artists, many=True)
        out = data_show(serializer.data)
        return JsonResponse(out, safe=False)
    
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        try:
            byte_string = data['name'].encode('utf-8')
            if isinstance(data['age'], (float, str, list, dict, tuple)):
                return HttpResponse("Input inválido",status=400)
        except:
            return HttpResponse("Input inválido",status=400)


        encoded_data = base64.b64encode(byte_string)
        encoded_data = encoded_data.decode('utf-8')
        coded = str(encoded_data[:22])
        data['artist_id'] = coded
        data['albums'] = 'https://t2-api-music.herokuapp.com/artists/'+data['artist_id']+'/albums'
        data['tracks'] = 'https://t2-api-music.herokuapp.com/artists/'+data['artist_id']+'/tracks'
        data['self_url'] = 'https://t2-api-music.herokuapp.com/artists/'+data['artist_id']
        serializer = ArtistSerializer(data=data)

        if serializer.is_valid():
            try:
                artist = Artist.objects.get(artist_id=data['artist_id'])
                out = data_show_unit(serializer.data)
                return JsonResponse(out, status=409)
            except:
                serializer.save()
                out = data_show_unit(serializer.data)
                return JsonResponse(out, status=201)

        return JsonResponse(serializer.errors, status=400)
    else:
        return HttpResponse("Método no permitido", status=405)

@csrf_exempt
def artist_detail(request, artist_id):
    try:
        artist = Artist.objects.get(artist_id=artist_id)

    except Artist.DoesNotExist:
        return HttpResponse("Artista no encontrado", status=404)

    if request.method == 'GET': #HACERLO SIN LISTA
        serializer = ArtistSerializer(artist)
        out = data_show_unit(serializer.data)
        return JsonResponse(out)

    elif request.method == 'DELETE':
        artist.delete()
        return HttpResponse(status=204)

    else:
        return HttpResponse("Método no permitido", status=405)

@csrf_exempt
def artist_albums(request, artist_id):
    
    if request.method == 'GET':
        try:
            artist = Artist.objects.get(artist_id=artist_id)

        except Artist.DoesNotExist:
            return HttpResponse("Artista no encontrado", status=404)

        album = Album.objects.all().filter(artist='https://t2-api-music.herokuapp.com/artists/'+artist_id)
        serializer = AlbumSerializer(album, many=True)
        out = data_show(serializer.data)
        return JsonResponse(out, safe=False)

    elif request.method == 'POST':
        try:
            try:
                artist = Artist.objects.get(artist_id=artist_id)

            except Artist.DoesNotExist:
                return HttpResponse("Artista no existe", status=422)
            
            data = JSONParser().parse(request)
            data['artist'] = 'https://t2-api-music.herokuapp.com/artists/'+artist_id
            string = data['name'] + ':' + artist_id
            
            if isinstance(data['genre'], (float, int, list, dict, tuple)):
                return HttpResponse("Input inválido",status=400)
        except:
            return HttpResponse("Input inválido",status=400)

        byte_string = string.encode('utf-8')
        encoded_data = base64.b64encode(byte_string)
        encoded_data = encoded_data.decode('utf-8')
        coded = str(encoded_data[:22])
        data['album_id'] = coded
        data['tracks'] = 'https://t2-api-music.herokuapp.com/albums/' + data['album_id'] + '/tracks'
        data['self_url'] = 'https://t2-api-music.herokuapp.com/albums/' + data['album_id']
        serializer = AlbumSerializer(data=data)

        if serializer.is_valid():
            try:
                album = Album.objects.get(album_id=data['album_id'])
                out = data_show_unit(serializer.data)
                return JsonResponse(out, status=409)
            except:
                serializer.save(artist_link = artist)
                out = data_show_unit(serializer.data)
                return JsonResponse(out, status=201)
        return JsonResponse(serializer.errors, status=400)

    else:
        return HttpResponse("Método no permitido", status=405)


@csrf_exempt
def artist_albums_play (request, artist_id):
    try: #Verifica que exista el artista
        artist = Artist.objects.get(artist_id=artist_id)

    except Artist.DoesNotExist:
        return HttpResponse("Artista no encontrado", status=404)

    if request.method == 'PUT':
        albums = Album.objects.all().filter(artist='https://t2-api-music.herokuapp.com/artists/'+artist_id)
        for album in albums:
            album_tracks_play(request, album.album_id)
        albums = Album.objects.all().filter(artist='https://t2-api-music.herokuapp.com/artists/'+artist_id)
        serializer = AlbumSerializer(albums, many=True)
        out = data_show(serializer.data)
        return JsonResponse(out, safe=False)

    else:
        return HttpResponse("Método no permitido", status=405)

@csrf_exempt
def artist_tracks (request, artist_id):
    try:
        Artist.objects.get(artist_id=artist_id)

    except Artist.DoesNotExist:
        return HttpResponse("Artista no encontrado", status=404)

    if request.method == 'GET':
        track = Track.objects.all().filter(artist='https://t2-api-music.herokuapp.com/artists/'+artist_id)
        serializer = TrackSerializer(track, many=True)
        out = data_show(serializer.data)
        return JsonResponse(out, safe=False)
    
    else:
        return HttpResponse("Método no permitido", status=405)


@csrf_exempt
def album_list(request):
    if request.method == 'GET':
        albums = Album.objects.all()
        serializer = AlbumSerializer(albums, many=True)
        out = data_show(serializer.data)
        return JsonResponse(out, safe=False)
    
    else:
        return HttpResponse("Método no permitido", status=405)

@csrf_exempt
def album_detail(request, album_id):
    try:
        album = Album.objects.get(album_id=album_id)

    except Album.DoesNotExist:
        return HttpResponse("Álbum no encontrado", status=404)

    if request.method == 'GET': #HACERLO SIN LISTA
        serializer = AlbumSerializer(album)
        out = data_show_unit(serializer.data)
        return JsonResponse(out)

    elif request.method == 'DELETE':
        album.delete()
        return HttpResponse(status=204)
    
    else:
        return HttpResponse("Método no permitido", status=405)

@csrf_exempt
def album_tracks(request, album_id):
    
    if request.method == 'GET':
        try:
            album = Album.objects.get(album_id=album_id)

        except Album.DoesNotExist:
            return HttpResponse("Álbum no encontrado", status=404)

        track = Track.objects.all().filter(album='https://t2-api-music.herokuapp.com/albums/'+album_id)
        serializer = TrackSerializer(track, many=True)
        out = data_show(serializer.data)
        return JsonResponse(out, safe=False)

    elif request.method == 'POST':
        try:
            data = JSONParser().parse(request)
            data['album'] = 'https://t2-api-music.herokuapp.com/albums/'+ album_id
            string = data['name'] + ':' + album_id
            if isinstance(data['duration'], (int, str, list, dict, tuple)):
                return HttpResponse("Input inválido",status=400)
        except:
            return HttpResponse("Input inválido",status=400)

        try:
            album = Album.objects.get(album_id=album_id)

        except Album.DoesNotExist:
            return HttpResponse("Álbum no existe", status=422)

        album_info = AlbumSerializer(album).data

        

        
        
        byte_string = string.encode('utf-8')
        encoded_data = base64.b64encode(byte_string)
        encoded_data = encoded_data.decode('utf-8')
        coded = str(encoded_data[:22])
        data['track_id'] = coded
        data['times_played'] = 0
        data['artist'] = album_info['artist']
        data['self_url'] = 'https://t2-api-music.herokuapp.com/tracks/' + data['track_id']
        serializer = TrackSerializer(data=data)

        if serializer.is_valid():
            try:
                track = Track.objects.get(track_id=data['track_id'])
                out = data_show_unit(serializer.data)
                return JsonResponse(out, status=409)
            except:
                serializer.save(album_link = album)
                out = data_show_unit(serializer.data)
                return JsonResponse(out, status=201)
        return JsonResponse(serializer.errors, status=400)

    else:
        return HttpResponse("Método no permitido", status=405)


@csrf_exempt
def album_tracks_play(request, album_id):
    try: #Verifica que exista el álbum
        album = Album.objects.get(album_id=album_id)

    except Album.DoesNotExist:
        return HttpResponse("Álbum no encontrado", status=404)

    if request.method == 'PUT':
        tracks = Track.objects.all().filter(album='https://t2-api-music.herokuapp.com/albums/'+album_id)
        for track in tracks:
            track_detail_play(request, track.track_id)
        tracks = Track.objects.all().filter(album='https://t2-api-music.herokuapp.com/albums/'+album_id)
        serializer = TrackSerializer(tracks, many=True)
        out = data_show(serializer.data)
        return JsonResponse(out, safe=False)
    
    else:
        return HttpResponse("Método no permitido", status=405)


@csrf_exempt
def track_list(request):
    if request.method == 'GET':
        tracks = Track.objects.all()
        serializer = TrackSerializer(tracks, many=True)
        out = data_show(serializer.data)
        return JsonResponse(out, safe=False)
    
    else:
        return HttpResponse("Método no permitido", status=405)


@csrf_exempt
def track_detail(request, track_id):
    try:
        track = Track.objects.get(track_id=track_id)

    except Track.DoesNotExist:
        return HttpResponse("Canción no encontrada", status=404)

    if request.method == 'GET': #HACERLO SIN LISTA
        serializer = TrackSerializer(track)
        out = data_show_unit(serializer.data)
        return JsonResponse(out)

    elif request.method == 'DELETE':
        track.delete()
        return HttpResponse(status=204)
    
    else:
        return HttpResponse("Método no permitido", status=405)

@csrf_exempt
def track_detail_play(request, track_id):
    try:
        track = Track.objects.get(track_id=track_id)

    except Track.DoesNotExist:
        return HttpResponse("Canción no encontrada", status=404)

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
            out = data_show_unit(serializer.data)
            return JsonResponse(out, status=200)
        return JsonResponse(serializer.errors, status=400) #Nunca debería mostrar este error

    else:
        return HttpResponse("Método no permitido", status=405)