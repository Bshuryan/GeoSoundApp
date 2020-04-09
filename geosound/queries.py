from django.db import connection
from geosound.models import Song
from geosound.models import Playlist
from geosound.models import User


# returns a list with all songs available


def get_lib():
    queryset = Song.objects.all()
    return queryset


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


def play_song(song_id, user_id):
    cursor = connection.cursor()
    try:
        cursor.callproc('play', [song_id, user_id])
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
        if user_search.lower() in instance.song_name.lower() or user_search.lower() in instance.song_artist.lower():
            filtered_songs.append(instance)
    return filtered_songs


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


# get user_id from request.session['user_id']
def create_playlist(user_id, playlist_name):
    cursor = connection.cursor()
    try:
        cursor.callproc('create_playlist', [user_id, playlist_name])
    finally:
        cursor.close()


def song_to_obj(song_lst):
    obj_list = []
    for s in song_lst:
        s_id = s[0]
        song_match = Song.objects.get(song_id__exact=s_id)
        obj_list.append(song_match)
    return obj_list


def sec_to_mins(seconds):
    minutes = str(int(seconds/60))
    remainder = str(seconds % 60)
    return minutes + ':' + remainder
