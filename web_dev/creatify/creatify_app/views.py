from django.contrib.auth import authenticate, login, logout
from django.middleware.csrf import get_token
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import render, redirect
from django.http import JsonResponse
from spotipy import oauth2, Spotify
from . import credentials
import json
import pandas as pd
import requests
from . import view_helper_functs

# def vic_view(request): #old, no longer used
#     sliders = [
#   {
#     "name": "Danceability",
#     "desc": "Danceability measures how suitable for dancing and is based on musical elements such as tempo, rhythm stability, beat and regularity.",
#     "low":"Low",
#     "medium":"Medium",
#     "high":"High"
#   },
#   {
#     "name": "Energy",
#     "desc": "Energy measures the intensity and activity based on loudness, timbre, and other factors.",
#     "low":"Calm",
#     "medium":"Average",
#     "high":"Energetic"
#   },
#   {
#     "name": "Valence",
#     "desc": "Valence is the positivity of the song i.e. happier songs have higher valence",
#     "low":"Meloncholic",
#     "medium":"Average",
#     "high":"Cheery"
#   },
#   {
#     "name": "Instrumentalness",
#     "desc": "Instrumentalness measures how much of the song is predominated with vocals or instruments",
#     "low":"Vocal",
#     "medium":"Average",
#     "high":"Instrumental"
#   },
#   {
#     "name": "Tempo",
#     "desc": "The speed of the track in beats per minute",
#     "low":"Slower",
#     "medium":"Average",
#     "high":"Faster"
#   }
# ]
#     genres = ['afrobeat', 'alt-Rock', 'alternative', 'ambient', 'anime', 'black-Metal', 'bluegrass', 'blues', 'bossanova', 'brazil', 'breakbeat', 'british', 'cantopop', 'chicago-House', 'children', 'chill', 'classical', 'club', 'comedy', 'country', 'dance', 'dancehall', 'death-Metal', 'deep-House', 'detroit-Techno', 'disco', 'disney', 'drum-and-Bass', 'dub', 'dubstep', 'edm', 'electro', 'electronic', 'emo', 'folk', 'forro', 'french', 'funk', 'garage', 'german', 'gospel', 'goth', 'grindcore', 'groove', 'grunge', 'guitar', 'happy', 'hard-Rock', 'hardcore', 'hardstyle', 'heavy-Metal', 'hip-Hop', 'holidays', 'honky-Tonk', 'house', 'idm', 'indian', 'indie', 'indie-Pop', 'industrial', 'iranian', 'j-Dance', 'j-Idol', 'j-Pop', 'j-Rock', 'jazz', 'k-Pop', 'kids', 'latin', 'latino', 'malay', 'mandopop', 'metal', 'metal-Misc', 'metalcore', 'minimal-Techno', 'movies', 'mpb', 'new-Age', 'new-Release', 'opera', 'pagode', 'party', 'philippines-Opm', 'piano', 'pop', 'pop-Film', 'post-Dubstep', 'power-Pop', 'progressive-House', 'psych-Rock', 'punk', 'punk-Rock', 'R-N-B', 'rainy-Day', 'reggae', 'reggaeton', 'road-trip', 'rock', 'rock-n-Roll', 'rockabilly', 'romance', 'sad', 'salsa', 'samba', 'sertanejo', 'show-Tunes', 'singer-Songwriter', 'ska', 'sleep', 'songwriter', 'soul', 'soundtracks', 'spanish', 'study', 'summer', 'swedish', 'synth-Pop', 'tango', 'techno', 'trance', 'trip-Hop', 'turkish', 'work-Out', 'world-Music']
#     return render(request, 'creatify_app/victoria.html', {'genres':genres, 'sliders':sliders})
def baserender(request): #add in top features function
  access_token = request.session.get('token').get('access_token')
  songs_dict = view_helper_functs.get_top_features(access_token)
  #add in top features function
  sliders = [
  {
    "Name": "danceability",
    "desc": "Danceability measures how suitable for dancing and is based on musical elements such as tempo, rhythm stability, beat and regularity.",
    "track_low":songs_dict['danceability'][0][14:],
    "track_high":songs_dict['danceability'][1][14:],
    "low":"Low",
    "medium":"Medium",
    "high":"High"
  },
  {
    "Name": "energy",
    "desc": "Energy measures the intensity and activity based on loudness, timbre, and other factors.",
    "track_low":songs_dict['energy'][0][14:],
    "track_high":songs_dict['energy'][1][14:],
    "low":"Calm",
    "medium":"Average",
    "high":"Energetic"
  },
  {
    "Name": "valence",
    "desc": "Valence is the positivity of the song i.e. happier songs have higher valence",
    "track_low":songs_dict['valence'][0][14:],
    "track_high":songs_dict['valence'][1][14:],
    "low":"Meloncholic",
    "medium":"Average",
    "high":"Cheery"
  },
  {
    "Name": "instrumentalness",
    "desc": "Instrumentalness measures how much of the song is predominated with vocals or instruments",
    "track_low":songs_dict['instrumentalness'][0][14:],
    "track_high":songs_dict['instrumentalness'][1][14:],
    "low":"Vocal",
    "medium":"Average",
    "high":"Instrumental"
  },
  {
    "Name": "tempo",
    "desc": "The speed of the track in beats per minute",
    "track_low":songs_dict['tempo'][0][14:],
    "track_high":songs_dict['tempo'][1][14:],
    "low":"Slower",
    "medium":"Average",
    "high":"Faster"
  }
]
  genres = ['afrobeat', 'alt-Rock', 'alternative', 'ambient', 'anime', 'black-Metal', 'bluegrass', 'blues', 'bossanova', 'brazil', 'breakbeat', 'british', 'cantopop', 'chicago-House', 'children', 'chill', 'classical', 'club', 'comedy', 'country', 'dance', 'dancehall', 'death-Metal', 'deep-House', 'detroit-Techno', 'disco', 'disney', 'drum-and-Bass', 'dub', 'dubstep', 'edm', 'electro', 'electronic', 'emo', 'folk', 'forro', 'french', 'funk', 'garage', 'german', 'gospel', 'goth', 'grindcore', 'groove', 'grunge', 'guitar', 'happy', 'hard-Rock', 'hardcore', 'hardstyle', 'heavy-Metal', 'hip-Hop', 'holidays', 'honky-Tonk', 'house', 'idm', 'indian', 'indie', 'indie-Pop', 'industrial', 'iranian', 'j-Dance', 'j-Idol', 'j-Pop', 'j-Rock', 'jazz', 'k-Pop', 'kids', 'latin', 'latino', 'malay', 'mandopop', 'metal', 'metal-Misc', 'metalcore', 'minimal-Techno', 'movies', 'mpb', 'new-Age', 'new-Release', 'opera', 'pagode', 'party', 'philippines-Opm', 'piano', 'pop', 'pop-Film', 'post-Dubstep', 'power-Pop', 'progressive-House', 'psych-Rock', 'punk', 'punk-Rock', 'R-N-B', 'rainy-Day', 'reggae', 'reggaeton', 'road-trip', 'rock', 'rock-n-Roll', 'rockabilly', 'romance', 'sad', 'salsa', 'samba', 'sertanejo', 'show-Tunes', 'singer-Songwriter', 'ska', 'sleep', 'songwriter', 'soul', 'soundtracks', 'spanish', 'study', 'summer', 'swedish', 'synth-Pop', 'tango', 'techno', 'trance', 'trip-Hop', 'turkish', 'work-Out', 'world-Music']
  return render(request, 'creatify_app/victoria.html', {'genres':genres, 'sliders':sliders})
# results page view
def result_view(request):
    if request.method == 'POST':
      body_unicode = request.body.decode('utf-8')
      body = json.loads(body_unicode)
      if body['nameChange']:
        print('new name',body['newName'])
        access_token = request.session.get('token').get('access_token')
        sp = Spotify(auth=access_token)
        sp.playlist_change_details(playlist_id=body['playlistID'],name = body['newName'])
      else:
        genres = body['genres']
        slider_values = body['slider_values']
        goal = body['goal']
        goal = int(goal)
        print('genres',genres)
        print('slider_values',slider_values)
        print('goal',goal)
        genres = [word.capitalize() for word in genres]
        request.session['selected_genres'] = genres
        access_token = request.session.get('token').get('access_token')
        playlist_titles, playlist_id = view_helper_functs.generate_playlist(access_token,genres,slider_values,goal )
        request.session['playlist_titles'] = playlist_titles
        request.session['playlist_id'] = playlist_id
        # below are the names for the slider values not the names themselves
        slider_values = view_helper_functs.convert_slider_vals(slider_values)
        request.session['slider_values'] = slider_values

        return render(request, 'creatify_app/results.html' )
    else:
      selected_genres = request.session.get('selected_genres')
      slider_values = request.session.get('slider_values')
      playlist_titles = request.session.get('playlist_titles')
      playlist_id = request.session.get('playlist_id')
      context = {'selected_genres': selected_genres, 'slider_values': slider_values, 'playlist_titles': playlist_titles, 'playlist_id':playlist_id, 'showbanner': True}
      print(context)
      return render(request, 'creatify_app/results.html', context)
# get spotify authorization
def auth_view(request):
    SCOPE = ('user-read-recently-played,user-library-read,user-read-currently-playing,playlist-read-private,playlist-modify-private,playlist-modify-public,user-read-email,user-modify-playback-state,user-read-private,user-read-playback-state,user-top-read')
    sp_oauth = oauth2.SpotifyOAuth(
        credentials.SPOTIPY_CLIENT_ID,
        credentials.SPOTIPY_CLIENT_SECRET,
        credentials.SPOTIPY_REDIRECT_URI,
        scope=SCOPE,
        cache_path='.spotifycache'
    )

    if request.GET.get('code'):
        # If the user grants permission, Spotify will redirect to this URL with a code.
        token = sp_oauth.get_access_token(request.GET['code'])
        request.session['token'] = token
        return redirect('creatify_app:base') # Redirect to your homepage.

    else:
        # If we don't have a token in the session, redirect the user to Spotify authorization page.
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)
# Login and Logout Views
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'creatify_app/main.html', {'form': form})
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'creatify_app/login.html', {'form': form})
def logout_view(request):
    logout(request)
    return redirect('login_view')

def change_playlist_name(request):
  '''
  input: sp, playlist_id, new_name 

  (new_name should be the id of the button)

  sp.playlist_change_details(playlist_id,name = new_name)
  
  '''
  if request.method == 'POST':
      title = request.POST.get('title')
      # Call the change_playlist_name() function with the selected title
      change_playlist_name(title)
      # Return a success JSON response
      return JsonResponse({'status': 'success'})
  # Return an error JSON response if the request method is not POST
  return JsonResponse({'status': 'error', 'message': 'Invalid request method'})