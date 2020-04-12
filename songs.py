
class SongDisplay():
    def __init__(self, song_id, song_name, song_artist, song_genre, song_duration):
        self.song_id = song_id
        self.song_name = song_name
        self.song_artist = song_artist
        self.song_genre = song_genre
        try:
            song_len = int(song_duration)
            self.song_duration = sec_to_mins(song_len)
        except (ValueError, TypeError):
            self.song_duration = song_duration


def sec_to_mins(seconds):
    minutes = str(int(int(seconds) / 60))
    remainder = str(int(seconds) % 60)
    if int(remainder) < 10:
        remainder = '0' + remainder
    return minutes + ':' + remainder