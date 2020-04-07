from django.urls import path
from . import views

urlpatterns = [
    # below is the page directly when the server is run: localhost8000:/
    path('', views.login_view, name='login'), # syntax: path('whatever is appended to the url', function name where view is found, name='function name'
    path('results', views.results_view, name='results'),
    path('search', views.search_lib_view, name='search'),
    path('new-user', views.new_user_view, name='new-user'),
    path('create-playlist', views.create_playlist_view, name='create-playlist')
]
