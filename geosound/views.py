from django.shortcuts import render
from django.http import HttpResponse
from geosound.login import validate_location
from geosound.login import create_user
import geosound.queries


# Create your views here.
def new_user_view(request):
    # fetch all this date from html at time that user presses button to create user
    # ** DISREGARD THE BELOW CODE IN NEW USER VIEW **
    city_name = 'Rochester'
    city_state = 'MI'
    usr_zip = '48308'
    usr_email = 'dummy3@gmail.com'
    usr_password = 'password123'
    usr_fname = 'John'
    usr_lname = 'Doe'
    usr_street = 'University Dr'
    usr_addr = '23'

    city_match = validate_location(city_name, city_state, usr_zip)
    context = {'title': -1}

    # valid city not found
    if city_match == -1:
        context['title'] = 'Error: Invalid location'
    else:
        context['title'] = city_match
        new_user = create_user(email=usr_email, password=usr_password, fname=usr_fname, lname=usr_lname,
                               street=usr_street, addr_num=usr_addr, zip_code=usr_zip, city_num=city_match)
        request.session['user_id'] = new_user
        request.session['results_id'] = 0

    return render(request, 'geosound/new_user.html', context)  # points to geosound/templates/geosound/login.html


def login_view(request):
    # the user id will be dynamically set here
    request.session['user_id'] = 1
    request.session['results_id'] = 101
    return render(request, 'geosound/login.html')


def create_playlist_view(request):
    return render(request, 'geosound/create_playlist.html')


""" 
    request.session['results_id'] codes:
        0 -> base library
        1 -> geosounds for request.session['user_id']
        2 -> search results for string passed to request.session['usr_search']
        100+ -> return data for playlist with id = request.session['results_id'] - 100

"""

# this will change a lot - ignore most
def results_view(request):
    results_code = request.session['results_id']
    playlists = geosound.queries.get_playlists(request.session['user_id'])
    # user_playlists = { play.playlist_id: play.playlist_name] for play in playlists }
    user_playlists = dict((p.playlist_id, p.playlist_name) for p in playlists)

    # display entire library - home page
    if results_code == 0:
        song_results = geosound.queries.get_lib()
        header = 'Library'
    # show geosounds for current user
    elif results_code == 1:
        song_results = geosound.queries.show_geosounds(request.session['user_id'])
        header = 'Geosounds - Top Ten Songs Near You'
    # show matching records for search results
    elif results_code == 2:
        user_input = request.GET['usr_input']
        header = 'Search Results'
        song_results = geosound.queries.search_library(user_input)
    # show all songs from selected playlist
    elif results_code >= 100:
        header = '*Insert Playlist Name Here*'
        playlist_id = results_code - 100
        song_results = geosound.queries.show_songs_in_playlist(playlist_id)
    else:
        song_results = geosound.queries.get_lib()

    context = {'song_list': song_results, 'page_header': header, 'usr_playlists': user_playlists}
    return render(request, 'geosound/home_lib.html', context)


def search_lib_view(request):
    request.session['results_id'] = 2
    return render(request, 'geosound/search_lib.html')
