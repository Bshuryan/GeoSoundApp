from django.test import TestCase
from django.db import connections
from django.db import connection
from geosound.models import Song
import itertools

# how to call a stored procedure with no parameters
def list_songs():
    cursor = connection.cursor()
    try:
        cursor.execute("call show_all_songs()")
        songs = cursor.fetchall()
        return songs
    finally:
        cursor.close()


# how to call a stored procedure with parameters
def play_song(user_id, song_id):
    cursor = connection.cursor()
    try:
        cursor.execute("call play(" + str(song_id) + ", " + str(user_id) + ")")
        # songs = list(itertools.chain.from_iterable(cursor.fetchall))
        return 0
    finally:
        cursor.close()


def main():
    list_songs()


if __name__ == '__main__':
    main()



