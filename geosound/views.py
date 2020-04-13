from django.shortcuts import render
from django.http import HttpResponse
from geosound.login import validate_location
from geosound.login import create_user
from geosound.login import validate_user
import geosound.queries
from geosound.models import Playlist
from geosound.models import Song
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
def new_user_view(request):
    return render(request, 'geosound/new_user.html')  # points to geosound/templates/geosound/login.html


# login page - default when first opening web page
def login_view(request):
    return render(request, 'geosound/login.html')


# home page
def home_library_view(request, origin):
    # returning user logging in - validate email and password
    if origin == 'returning-user':
        user_password = request.GET.get('usr_password', '')
        user_email = request.GET.get('usr_email', '')
        user_id = validate_user(user_email, user_password)

        # invalid login information - redirect to login page
        if user_id == -1:
            response = redirect('login')
            return response
        # valid login - continue to home page and set active user
        else:
            request.session['user_id'] = user_id

    # new user creating an account - validate their location and create a new USER instance
    elif origin == 'new-user':
        # get information from the fields that the user inputs
        usr_email = request.GET.get('email', '')
        usr_password = request.GET.get('password', '')
        usr_fname = request.GET.get('fname', '')
        usr_lname = request.GET.get('lname', '')
        full_addr = request.GET.get('address', '')

        # invalid input
        if not full_addr or not usr_email or not usr_fname or not usr_lname or not usr_password:
            return redirect('new-user')

        usr_addr = full_addr.split()[0]
        usr_street = ''.join(full_addr.split()[1:])
        usr_zip = request.GET.get('zip_code', '')
        city_state = request.GET.get('state', '')
        city_name = request.GET.get('city', '')

        # invalid input
        if not usr_street or not usr_zip or not city_state or not city_name:
            return redirect('new-user')

        # returns a valid city_id if location is found, otherwise returns -1
        city_match = validate_location(city_name, city_state, usr_zip)

        # valid city not found - return back to create user page
        if city_match == -1:
            response = redirect('new-user')
            return response
        # valid city found, proceed to create new user
        else:
            # returns the user_id for the newly created user object
            new_user = create_user(email=usr_email, password=usr_password, fname=usr_fname, lname=usr_lname,
                                   street=usr_street, addr_num=usr_addr, zip_code=usr_zip, city_num=city_match)
            request.session['user_id'] = new_user

    else:
        # check if need to delete a playlist
        try:
            playlist_id = int(origin)
            geosound.queries.delete_playlist(playlist_id)
        # nothing to do
        except ValueError:
            pass

    song_results = geosound.queries.get_lib()
    context = {'song_list': song_results}
    return render(request, 'geosound/home_library.html', context)


# view to create playlists
def create_playlist_view(request):
    return render(request, 'geosound/create_playlist.html')


# view corresponding to the search page
def search_lib_view(request):
    return render(request, 'geosound/search_lib.html')


# view to display search results
def search_results_view(request):
    user_input = request.GET['usr_input']
    search_results = geosound.queries.search_library(user_input)
    context = {'song_list': search_results}
    return render(request, 'geosound/search_results.html', context)


# view to display songs in a selected playlist
def playlist_results_view(request, playlist_id, song_id):
    playlist_id = int(playlist_id)
    song_id = int(song_id)
    if song_id != 0:
        geosound.queries.add_song_to_playlist(playlist_id, song_id)
    playlist_obj = Playlist.objects.get(playlist_id=playlist_id)
    playlist_title = playlist_obj.playlist_name
    song_results = geosound.queries.show_songs_in_playlist(playlist_id)
    context = {'song_list': song_results, 'playlist_name': playlist_title}
    return render(request, 'geosound/playlist_results.html', context)


# view to display geosounds for current user
def geosounds_view(request):
    song_results = geosound.queries.show_geosounds(request.session['user_id'])
    context = {'song_list': song_results}
    return render(request, 'geosound/geosounds.html', context)


# view to select playlist to add a song to
def select_playlist_to_add_view(request, song_id):
    playlists = geosound.queries.get_playlists(request.session['user_id'])
    user_playlists = dict((p.playlist_id, p.playlist_name) for p in playlists)
    context = {'usr_playlists': user_playlists, 'song_id': song_id}
    return render(request, 'geosound/select_playlist_to_add.html', context)


# view to select playlist to display
def select_playlist_to_display_view(request, origin):
    # call create new playlist, get user's playlist name
    if origin == 'from-create':
        playlist_name = request.GET.get('playlist_name', '')
        if not playlist_name:
            return redirect('create-playlist')
        else:
            geosound.queries.create_playlist(request.session['user_id'], playlist_name)

    playlists = geosound.queries.get_playlists(request.session['user_id'])
    user_playlists = dict((p.playlist_id, p.playlist_name) for p in playlists)

    context = {'usr_playlists': user_playlists}
    return render(request, 'geosound/select_playlist_to_display.html', context)


# view when playing a song
def play_song_view(request, song_id):
    geosound.queries.play_song(int(song_id), request.session['user_id'])
    song_obj = Song.objects.get(song_id=song_id)
    song_name = song_obj.song_name
    song_artist = song_obj.song_artist
    context = {'song_name': song_name, 'song_artist': song_artist}
    return render(request, 'geosound/play_song.html', context)
