from django.urls import path
from .views import artist_list, album_list, track_list, artist_detail, album_detail, track_detail, artist_albums, artist_tracks, album_tracks, artist_albums_play, album_tracks_play, track_detail_play

urlpatterns = [
    path('artists', artist_list), #Muestra todos los artistas
    path('artists/<str:artist_id>', artist_detail), #Muestra un artista en especifico
    path('artists/<str:artist_id>/albums', artist_albums), #Muestra los albumnes de un artista
    path('artists/<str:artist_id>/albums/play', artist_albums_play), #Reproduce todas las canciones de este album
    path('artists/<str:artist_id>/tracks', artist_tracks), #Muestra todas las cacniones de un artista
    path('albums', album_list), #Muestra todos los albumes
    path('albums/<str:album_id>', album_detail), #Muestra un album en especifico
    path('albums/<str:album_id>/tracks', album_tracks), #Muestra todas las canciiones de un album
    path('albums/<str:album_id>/tracks/play', album_tracks_play),
    path('tracks', track_list),
    path('tracks/<str:track_id>', track_detail),
    path('tracks/<str:track_id>/play', track_detail_play),
]