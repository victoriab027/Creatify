import spotipy
import credentials

# Gain access to spotify API
#SCOPE = ('user-read-recently-played,user-library-read,user-read-currently-playing,playlist-read-private,playlist-modify-private,playlist-modify-public,user-read-email,user-modify-playback-state,user-read-private,user-read-playback-state')
#sp_oauth = oauth2.SpotifyOAuth(credentials.SPOTIPY_CLIENT_ID, credentials.SPOTIPY_CLIENT_SECRET, credentials.SPOTIPY_REDIRECT_URI, scope=SCOPE)


auth_manager = SpotifyClientCredentials(client_id=credentials.SPOTIPY_CLIENT_ID, client_secret=credentials.SPOTIPY_CLIENT_SECRET)
sp = spotipy.Spotify(auth_manager=auth_manager)