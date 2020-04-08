from django.shortcuts import render
from django.http import HttpResponse
from geosound.login import validate_location
from geosound.login import create_user
from geosound.login import validate_user
import geosound.queries
from django.shortcuts import redirect
from .forms import ReturningUserForm


# Create your views here.
def new_user_view(request):
    request.session['returning_usr'] = 0
    return render(request, 'geosound/new_user.html')  # points to geosound/templates/geosound/login.html


def login_view(request):
    # the user id will be dynamically set here - manually setting for testing purposes
    request.session['returning_usr'] = 1
    return render(request, 'geosound/login.html')


def home_library_view(request):
    # returning user logging in - validate email and password
    if request.session['returning_usr'] == 1:
        user_email = 'dummy@gmail.com'
        user_password = 'password'
        # *** GET EMAIL AND PASSWORD FROM FORM HERE ***
        # user_email = GET EMAIL FROM HTML
        # user_password = GET PASSWORD FROM HTML
        user_id = validate_user(user_email, user_password)

        # invalid login information - redirect to login page
        if user_id == -1:
            response = redirect('login')
            return response
        # valid login - continue to home page and set active user
        else:
            request.session['user_id'] = user_id

    # new user creating an account - validate their location and create a new USER instance
    else:
        pass
        # get information from the fields that the user inputs
        """"
        usr_email = *GET EMAIL FIELD HERE*
        usr_password = *PASSWORD*
        usr_fname = *FIRST NAME*
        usr_lname = *LAST NAME*
        full_addr = *ENTIRE ADDRESS FIELD*
        usr_addr = full_addr.split()[0]
        usr_street = ''.join(full_addr.split()[1:])
        usr_zip = *ZIP CODE*
        
        
        # returns a valid city_id if location is found, otherwise returns -1
        city_match = validate_location(city_name, city_state, usr_zip)


        # valid city not found - return back to create user page
        if city_match == -1:
            response = redirect('new-user')
        # valid city found, proceed to create new user
        else:
            # returns the user_id for the newly created user object
            new_user = create_user(email=usr_email, password=usr_password, fname=usr_fname, lname=usr_lname,
                                   street=usr_street, addr_num=usr_addr, zip_code=usr_zip, city_num=city_match)
            request.session['user_id'] = new_user
            """

    request.session['returning_user'] = -1
    song_results = geosound.queries.get_lib()
    context = {'song_list': song_results }
    return render(request, 'geosound/home_library.html', context)


def create_playlist_view(request):
    return render(request, 'geosound/create_playlist.html')


def search_lib_view(request):
    return render(request, 'geosound/search_lib.html')


def search_results_view(request):
    # *** error with this line of code below ***
    user_input = request.GET['usr_input']

    search_results = geosound.queries.search_library(user_input)
    context = {'song_list': search_results}
    return render(request, 'geosound/search_results.html', context)


def playlist_results_view(request):
    header = '*Insert Playlist Name Here*'
    # this will be dynamically set
    playlist_id = 1
    song_results = geosound.queries.show_songs_in_playlist(playlist_id)
    context = {'song_list': song_results, 'playlist_name': header}
    return render(request, 'geosound/playlist_results.html', context)


def geosounds_view(request):
    song_results = geosound.queries.show_geosounds(request.session['user_id'])
    context = {'song_list': song_results}
    return render(request, 'geosound/geosounds.html', context)


def select_playlist_to_add_view(request):
    playlists = geosound.queries.get_playlists(request.session['user_id'])
    user_playlists = dict((p.playlist_id, p.playlist_name) for p in playlists)
    context = {'usr_playlists': user_playlists}
    return render(request, 'geosound/select_playlist_to_add.html', context)


def select_playlist_to_display_view(request):
    playlists = geosound.queries.get_playlists(request.session['user_id'])
    user_playlists = dict((p.playlist_id, p.playlist_name) for p in playlists)
    context = {'usr_playlists': user_playlists}
    return render(request, 'geosound/select_playlist_to_display.html', context)
