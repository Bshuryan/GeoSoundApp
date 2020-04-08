from django.urls import path
from . import views

urlpatterns = [
    # below is the page directly when the server is run: localhost8000:/
    path('', views.login_view, name='login'),
    path('home-library', views.home_library_view, name='home-library'),
    path('search', views.search_lib_view, name='search'),
    path('search-results', views.search_results_view, name='search-results'),
    path('new-user', views.new_user_view, name='new-user'),
    path('create-playlist', views.create_playlist_view, name='create-playlist'),
    path('playlist-results', views.playlist_results_view, name='playlist-results'),
    path('select-playlist-to-display', views.select_playlist_to_display_view, name='select-playlist-to-display'),
    path('select-playlist-to-add', views.select_playlist_to_add_view, name='select-playlist-to-add'),
    path('geosounds', views.geosounds_view, name='geosounds')

]
