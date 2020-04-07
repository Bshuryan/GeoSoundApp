from django.contrib import admin
from geosound.models import City
from geosound.models import Location
from geosound.models import User
from geosound.models import Song
from geosound.models import SongInPlaylist
from geosound.models import Playlist
from geosound.models import UserPlayingSong

# Register your models here.
admin.site.register(City)
admin.site.register(User)
admin.site.register(UserPlayingSong)
admin.site.register(Playlist)
admin.site.register(SongInPlaylist)
admin.site.register(Song)
admin.site.register(Location)