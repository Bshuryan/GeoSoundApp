from django.db import connection
from geosound.models import Song
from geosound.models import Playlist
from geosound.models import User
from songs import SongDisplay
from songs import sec_to_mins


# returns a list with all songs available
def get_lib():
    display_songs = []
    queryset = Song.objects.all()
    for obj in queryset:
        display_songs.append(song_to_display(obj))
    return display_songs


# calls show_geosounds database stored procedure
def show_geosounds(usr_id):
    cursor = connection.cursor()
    try:
        cursor.callproc('show_geosounds', [usr_id])
        songs = cursor.fetchall()
        songs_list = [list(song) for song in songs]
        obj_lst = song_to_obj(songs_list)
        return obj_lst
    finally:
        cursor.close()

# calls play stored procedure
def play_song(song_id, user_id):
    cursor = connection.cursor()
    try:
        cursor.callproc('play', [song_id, user_id])
    finally:
        cursor.close()


# calls play_from_playlist stored procedure
def play_song_from_playlist(song_id, user_id, playlist_id):
    cursor = connection.cursor()
    try:
        cursor.callproc('play_from_playlist', [song_id, user_id, playlist_id])
    finally:
        cursor.close()


# returns all playlists associated with the given user id
def get_playlists(usr_id):
    current_user = User.objects.get(user_id=usr_id)
    playlists = list(Playlist.objects.filter(user=current_user))
    return playlists


# returns all records in SONG table where either the song artist or song name matches input provided by the user
def search_library(user_search):
    entire_lib = get_lib()
    filtered_songs = []

    for instance in entire_lib:
        if user_search.lower() in instance.song_name.lower() or user_search.lower() in instance.song_artist.lower():
            filtered_songs.append(song_to_display(instance))
    return filtered_songs


# calls show_songs_in_playlist stored procedure
def show_songs_in_playlist(playlist_id):
    cursor = connection.cursor()
    try:
        cursor.callproc('show_songs_in_playlist', [playlist_id])
        songs = cursor.fetchall()
        songs_list = [list(song) for song in songs]
        obj_list = song_to_obj(songs_list)
        return obj_list
    finally:
        cursor.close()


# calls add_song_to_playlist stored procedure
def add_song_to_playlist(p_id, s_id):
    cursor = connection.cursor()
    try:
        cursor.callproc('add_song_to_playlist', [s_id, p_id])
    finally:
        cursor.close()


# calls create_playlist stored procedure from database
def create_playlist(user_id, playlist_name):
    cursor = connection.cursor()
    try:
        cursor.callproc('create_playlist', [user_id, playlist_name])
    finally:
        cursor.close()


# calls delete_playlist stored procedure
def delete_playlist(playlist_id):
    cursor = connection.cursor()
    try:
        cursor.callproc('delete_playlist', [playlist_id])
    finally:
        cursor.close()


# converts list of songs in array form to list of SONG objects
def song_to_obj(song_lst):
    obj_list = []
    for s in song_lst:
        s_id = s[0]
        song_match = Song.objects.get(song_id__exact=s_id)
        song_display = song_to_display(song_match)
        obj_list.append(song_display)
    return obj_list


# converts SONG object to SongDisplay object, which modifies data for visual purposes
def song_to_display(song_match):
    return SongDisplay(song_match.song_id, song_match.song_name, song_match.song_artist, song_match.song_genre,
                       song_match.song_duration)




