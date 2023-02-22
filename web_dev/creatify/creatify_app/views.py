from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import render, redirect
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
    genres = ['acoustic', 'afrobeat', 'alt-rock', 'alternative', 'ambient', 'anime', 'black-metal', 'bluegrass', 'blues', 'bossanova', 'brazil', 'breakbeat', 'british', 'cantopop', 'chicago-house', 'children', 'chill', 'classical', 'club', 'comedy', 'country', 'dance', 'dancehall', 'death-metal', 'deep-house', 'detroit-techno', 'disco', 'disney', 'drum-and-bass', 'dub', 'dubstep', 'edm', 'electro', 'electronic', 'emo', 'folk', 'forro', 'french', 'funk', 'garage', 'german', 'gospel', 'goth', 'grindcore', 'groove', 'grunge', 'guitar', 'happy', 'hard-rock', 'hardcore', 'hardstyle', 'heavy-metal', 'hip-hop', 'holidays', 'honky-tonk', 'house', 'idm', 'indian', 'indie', 'indie-pop', 'industrial', 'iranian', 'j-dance', 'j-idol', 'j-pop', 'j-rock', 'jazz', 'k-pop', 'kids', 'latin', 'latino', 'malay', 'mandopop', 'metal', 'metal-misc', 'metalcore', 'minimal-techno', 'movies', 'mpb', 'new-age', 'new-release', 'opera', 'pagode', 'party', 'philippines-opm', 'piano', 'pop', 'pop-film', 'post-dubstep', 'power-pop', 'progressive-house', 'psych-rock', 'punk', 'punk-rock', 'r-n-b', 'rainy-day', 'reggae', 'reggaeton', 'road-trip', 'rock', 'rock-n-roll', 'rockabilly', 'romance', 'sad', 'salsa', 'samba', 'sertanejo', 'show-tunes', 'singer-songwriter', 'ska', 'sleep', 'songwriter', 'soul', 'soundtracks', 'spanish', 'study', 'summer', 'swedish', 'synth-pop', 'tango', 'techno', 'trance', 'trip-hop', 'turkish', 'work-out', 'world-music']
    return render(request, 'creatify_app/main.html', {'genres':genres, 'sliders':sliders})
# results page view
def result_view(request):
    if request.method == 'POST':
      genres = request.POST.getlist('genres')
      slider_values = request.POST.get('slider_values')
      return render(request, 'creatify_app/results.html', {'selected_genres': genres, 'slider_values':slider_values})
    else:
      return render(request, 'creatify_app/results.html')
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
