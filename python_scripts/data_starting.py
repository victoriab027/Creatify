# importing all necessary packages
import json
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import credentials
import os

auth_manager = SpotifyClientCredentials(client_id=credentials.SPOTIPY_CLIENT_ID, client_secret=credentials.SPOTIPY_CLIENT_SECRET)
sp = spotipy.Spotify(auth_manager=auth_manager)

# CHANGE THIS TO THE FILE WANTED
p1 = open('/Users/victoria/Documents/me/MusicDataAnalysis/data/raw/data/mpd.slice.0-999.json')
data = json.load(p1)

playlists_data = data['playlists']

playlist_features_list = ["name","tracks","artists",'avg_danceability', 'avg_energy',
       'avg_loudness', 'avg_acousticness', 'avg_instrumentalness','avg_liveness', 'avg_valence' ,'avg_tempo']
playlists = pd.DataFrame(columns = playlist_features_list)

for p in range(0,1):
    # get the tracks and artists
    playlist_tracks = []
    artists = []
    for i in range(len(data['playlists'][p]['tracks'])):
        song_id = data['playlists'][p]['tracks'][i]['track_uri']
        song_id = song_id.replace("spotify:track:", "")
        playlist_tracks.append(song_id)
        artist_id = data['playlists'][p]['tracks'][i]['artist_uri']
        artist_id = artist_id.replace("spotify:artist:", "")
        artists.append(artist_id)
    
    audio_features = []
    # Loop through every track in the playlist, extract features and append the features to the playlist df
    for track in playlist_tracks:
        # Get audio features
        audio_features.append(sp.audio_features(track))
    audio_keys = []
    for d in audio_features[0]:
        audio_keys.extend(d.keys())
    audio_features_df = pd.DataFrame(audio_features[0], columns = audio_keys)
    for x in range(1, len(audio_features)):
        audio_features_df_single = pd.DataFrame(audio_features[x], columns = audio_keys)
        audio_features_df = pd.concat([audio_features_df, audio_features_df_single], ignore_index = True)

    # take the lists and make them into a strong
    artists = ' '.join(artists)
    playlist_tracks = ' '.join(playlist_tracks)

    playlist_data = {'name': data['playlists'][p]['name'],
        'tracks': playlist_tracks,
        'artists': artists,
        'avg_danceability': audio_features_df['danceability'].mean(),
        'avg_energy':audio_features_df['energy'].mean(),
       'avg_loudness': audio_features_df['loudness'].mean(),
        'avg_acousticness': audio_features_df['acousticness'].mean(), 
        'avg_instrumentalness': audio_features_df['instrumentalness'].mean(),
        'avg_liveness': audio_features_df['liveness'].mean(),
        'avg_valence' : audio_features_df['valence'].mean() ,
        'avg_tempo':  audio_features_df['tempo'].mean()}
    playlist_df = pd.DataFrame(playlist_data, index = [0])

    playlists = pd.concat([playlists, playlist_df], axis = 0, ignore_index = True)

    # For every playlist, add it to the CSV
    playlists.to_csv('playlists 0-999.csv', index=False)
    #name = "playlists 0-999.csv"
  #  directory = 'playlist_data'
   # filename = os.path.join(directory, name)
   # playlists.to_csv(filename, index=False)