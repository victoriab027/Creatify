import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import argparse
import logging
import spotipy
import pandas as pd
import numpy as np
import requests
from spotipy import oauth2
import re

import credentials

### BEGIN AUTHETIFCATION HERE

# Gain access to mainupation
SCOPE = ('user-read-recently-played,user-library-read,user-read-currently-playing,playlist-read-private,playlist-modify-private,playlist-modify-public,user-read-email,user-modify-playback-state,user-read-private,user-read-playback-state')
sp_oauth = oauth2.SpotifyOAuth(credentials.SPOTIPY_CLIENT_ID,credentials.SPOTIPY_CLIENT_SECRET, credentials.SPOTIPY_REDIRECT_URI ,scope=SCOPE )

#click "Accept" in your browser when the auth window pops up
code = sp_oauth.get_auth_response(open_browser=True)
token = sp_oauth.get_access_token(code)
refresh_token = token['refresh_token']
sp = spotipy.Spotify(auth=token['access_token'])
username = sp.current_user()['id']


#### BEGIN CODE HERE
def find_and_filter(settings, genres_list, sp):
    #FINDING
    results = sp.recommendations(seed_genres=genres_list, limit=100)
    #create an empty dataframe
    song_features_list = ["artist","album","track_name",  "track_id","danceability","energy","key","loudness","mode", "speechiness","instrumentalness","liveness","valence","tempo", "duration_ms","time_signature"]
    song_df = pd.DataFrame(columns = song_features_list)
    tracks = results["tracks"]


    for track in tracks:
        # Create empty dict
        playlist_features = {}
        playlist_features["artist"] = track["album"]["artists"][0]["name"]
        playlist_features["album"] = track["album"]["name"]
        playlist_features["track_name"] = track["name"]
        playlist_features["track_id"] = track["id"]
        
        # Get audio features
        audio_features = sp.audio_features(playlist_features["track_id"])[0]
        for feature in song_features_list[4:]:
            playlist_features[feature] = audio_features[feature]
        
        # Concat the dfs
        track_df = pd.DataFrame(playlist_features, index = [0])
        song_df = pd.concat([song_df, track_df], ignore_index = True)
    
    #FILTERING
    for index, setting in settings.iterrows():
        if setting["On"]:
            if setting["Level"] > 0:
                song_df = song_df[(song_df[setting["Name"]] >= song_df[setting["Name"]].mean())]
            elif setting["Level"] < 0:
                song_df = song_df[(song_df[setting["Name"]] <= song_df[setting["Name"]].mean())]
            else: #medium
                var = song_df[setting["Name"]].var()
                song_df = song_df[(song_df[setting["Name"]] >= song_df[setting["Name"]].mean()-2*var) & (song_df[setting["Name"]] <= song_df[setting["Name"]].mean()+2*var)]
    return song_df

def generate_playlist(generes_list, settings_df, goal, sp):
    final_df = find_and_filter(settings_df,generes_list,sp)
    while (len(final_df) < goal):
        getter = find_and_filter(settings_df,generes_list,sp)
        final_df = pd.concat([final_df, getter], ignore_index = True)

    # TODO: PLAYLIST NAMER
    #creating your playlist
    pl_name = 'comp_generated'
    result = sp.user_playlist_create(username,
    name=pl_name)
    playlist_id = result['id']

    logger = logging.getLogger('examples.add_tracks_to_playlist')
    logging.basicConfig(level='DEBUG')
    scope = 'playlist-modify-public'
    tracks = final_df["track_id"]
    sp.user_playlist_add_tracks(username, playlist_id=playlist_id, tracks=tracks)