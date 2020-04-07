from django.db import connection
from geosound.models import Song
from geosound.models import Playlist
from geosound.models import User


# returns a list with all songs available
def get_lib():
    cursor = connection.cursor()
    try:
        cursor.execute("call show_all_songs()")
        songs = list(cursor.fetchall())
        songs_list = [list(song) for song in songs]
        return songs_list
    finally:
        cursor.close()


def show_geosounds(usr_id):
    cursor = connection.cursor()
    try:
        cursor.callproc('show_geosounds', [usr_id])
        songs = cursor.fetchall()
        songs_list = [list(song) for song in songs]
        return songs_list
    finally:
        cursor.close()


# returns all playlists associated with the given user id
def get_playlists(usr_id):
    current_user = User.objects.get(user_id=usr_id)
    playlists = list(Playlist.objects.filter(user=current_user))
    return playlists


def search_library(user_search):
    entire_lib = get_lib()
    filtered_songs = []

    for instance in entire_lib:
        if user_search.lower() in instance[1].lower() or user_search.lower() in instance[2].lower():
            filtered_songs.append(instance)

    return filtered_songs


def show_songs_in_playlist(playlist_id):
    cursor = connection.cursor()
    try:
        cursor.callproc('show_songs_in_playlist', [playlist_id])
        songs = cursor.fetchall()
        songs_list = [list(song) for song in songs]
        return songs_list
    finally:
        cursor.close()
