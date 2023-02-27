from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import render, redirect
from spotipy import oauth2, Spotify
from . import credentials
import json
#from .running import generate_playlist
# settings genres goal sp
# hard code sp for now
# run notebook 6
#rendering base page view
def baserender(request):
    sliders = [
  {
    "name": "Danceability",
    "desc": "Danceability measures how suitable for dancing and is based on musical elements such as tempo, rhythm stability, beat and regularity.",
    "low":"Low",
    "medium":"Medium",
    "high":"High"
  },
  {
    "name": "Energy",
    "desc": "Energy measures the intensity and activity based on loudness, timbre, and other factors.",
    "low":"Calmer",
    "medium":"Average",
    "high":"Energetic"
  },
  {
    "name": "Valence",
    "desc": "Valence is the positivity of the song i.e. happier songs have higher valence",
    "low":"Meloncholic",
    "medium":"Average",
    "high":"Cheery"
  },
  {
    "name": "Instrumentalness",
    "desc": "Instrumentalness measures how much of the song is predominated with vocals or instruments",
    "low":"Vocal",
    "medium":"Average",
    "high":"Instrumental"
  },
  {
    "name": "Tempo",
    "desc": "The speed of the track in beats per minute",
    "low":"Slower",
    "medium":"Average",
    "high":"Faster"
  }
]
    genres = ['afrobeat', 'alt-Rock', 'alternative', 'ambient', 'anime', 'black-Metal', 'bluegrass', 'blues', 'bossanova', 'brazil', 'breakbeat', 'british', 'cantopop', 'chicago-House', 'children', 'chill', 'classical', 'club', 'comedy', 'country', 'dance', 'dancehall', 'death-Metal', 'deep-House', 'detroit-Techno', 'disco', 'disney', 'drum-and-Bass', 'dub', 'dubstep', 'edm', 'electro', 'electronic', 'emo', 'folk', 'forro', 'french', 'funk', 'garage', 'german', 'gospel', 'goth', 'grindcore', 'groove', 'grunge', 'guitar', 'happy', 'hard-Rock', 'hardcore', 'hardstyle', 'heavy-Metal', 'hip-Hop', 'holidays', 'honky-Tonk', 'house', 'idm', 'indian', 'indie', 'indie-Pop', 'industrial', 'iranian', 'j-Dance', 'j-Idol', 'j-Pop', 'j-Rock', 'jazz', 'k-Pop', 'kids', 'latin', 'latino', 'malay', 'mandopop', 'metal', 'metal-Misc', 'metalcore', 'minimal-Techno', 'movies', 'mpb', 'new-Age', 'new-Release', 'opera', 'pagode', 'party', 'philippines-Opm', 'piano', 'pop', 'pop-Film', 'post-Dubstep', 'power-Pop', 'progressive-House', 'psych-Rock', 'punk', 'punk-Rock', 'R-N-B', 'rainy-Day', 'reggae', 'reggaeton', 'road-trip', 'rock', 'rock-n-Roll', 'rockabilly', 'romance', 'sad', 'salsa', 'samba', 'sertanejo', 'show-Tunes', 'singer-Songwriter', 'ska', 'sleep', 'songwriter', 'soul', 'soundtracks', 'spanish', 'study', 'summer', 'swedish', 'synth-Pop', 'tango', 'techno', 'trance', 'trip-Hop', 'turkish', 'work-Out', 'world-Music']
    return render(request, 'creatify_app/main.html', {'genres':genres, 'sliders':sliders})
# results page view
def result_view(request):
    if request.method == 'POST':
      genres = request.POST.getlist('genres')
      slider_values = request.POST.get('slider_values')
      genres = json.loads(genres[0])
      genres = [word.capitalize() for word in genres]
      slider_values = json.loads(slider_values)
      slider_values = convert_slider_vals(slider_values)
      request.session['selected_genres'] = genres
      request.session['slider_values'] = slider_values
      return render(request, 'creatify_app/results.html')
    else:
      selected_genres = request.session.get('selected_genres')
      slider_values = request.session.get('slider_values')
      context = {'selected_genres': selected_genres, 'slider_values': slider_values}
      return render(request, 'creatify_app/results.html', context)
def convert_slider_vals(slider_list):
  print(slider_list)
  for slider in slider_list:
    if not slider['On']:
      slider["Level"] = "skip"
      continue
    if 'Danceability' in slider['name']:
      if slider["Level"] == -1:
        slider["Level"] = "Low"+ f" {slider['name']}"
      elif slider["Level"] == 0:
        slider["Level"] = "Medium"+ f" {slider['name']}"
      elif slider['Level'] == 1:
        slider["Level"] = "High"+ f" {slider['name']}"
    elif 'Energy' in slider['name']:
      if slider["Level"] == -1:
        slider["Level"] = "Calmer"+ f" {slider['name']}"
      elif slider["Level"] == 0:
        slider["Level"] = "Average"+ f" {slider['name']}"
      elif slider['Level'] == 1:
        slider["Level"] = "Energetic"
    elif 'Tempo' in slider['name']:
      if slider["Level"] == -1:
        slider["Level"] = "Slower"+ f" {slider['name']}"
      elif slider["Level"] == 0:
        slider["Level"] = "Average"+ f" {slider['name']}"
      elif slider['Level'] == 1:
        slider["Level"] = "Faster"+ f" {slider['name']}"
    elif 'Instrumentalness' in slider['name']:
      if slider["Level"] == -1:
        slider["Level"] = "Vocal"
      elif slider["Level"] == 0:
        slider["Level"] = "Average"+ f" {slider['name']}"
      elif slider['Level'] == 1:
        slider["Level"] = "Instrumental"
    elif 'Valence' in slider['name']:
      if slider["Level"] == -1: #Meloncholic
        slider["Level"] = "Meloncholic"
      elif slider["Level"] == 0:
        slider["Level"] = "Average"+ f" {slider['name']}"
      elif slider['Level'] == 1:
        slider["Level"] = "Cheery"
  return slider_list
# get spotify authorization
def auth_view(request):
  SCOPE = ('user-read-recently-played,user-library-read,user-read-currently-playing,playlist-read-private,playlist-modify-private,playlist-modify-public,user-read-email,user-modify-playback-state,user-read-private,user-read-playback-state')
  sp_oauth = oauth2.SpotifyOAuth(credentials.SPOTIPY_CLIENT_ID,credentials.SPOTIPY_CLIENT_SECRET, credentials.SPOTIPY_REDIRECT_URI ,scope=SCOPE )
  code = sp_oauth.get_auth_response(open_browser=True)
  token = sp_oauth.get_access_token(code)
  sp = Spotify(auth=token['access_token'])
  request.session['sp'] = sp
  request.session['user_id'] = sp.current_user()['id']
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
    return render(request, 'creatify_app/base.html', {'form': form})
def logout_view(request):
    logout(request)
    return redirect('login_view')
