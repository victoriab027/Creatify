import json
import pandas as pd
from spotipy import oauth2
import re
import credentials
import spotipy
import lyricsgenius
import requests
from empath import Empath
import numpy as np
import os
from spotipy.oauth2 import SpotifyClientCredentials


genius = lyricsgenius.Genius('i5KouOqTHCpdyW02rmaURbw1C2MUGVw-cayXvf0_VAHHmDlYqOXbA2c7iRp-NMxK', verbose=False, retries = 3)
starter = 617

def analyze_playlist(tracks, sp):
    
    # Create empty dataframe
    playlist_features_list = ["danceability","energy","loudness", "speechiness","instrumentalness","liveness"]
    
    playlist_df = pd.DataFrame(columns = playlist_features_list)
    
    # Loop through every track in the playlist, extract features and append the features to the playlist df
    for track in tracks:
        # Get audio features
        try: 
            audio_features = sp.audio_features(track)
        except requests.exceptions.Timeout:
            nans = []
            for x in range(len(playlist_features_list)):
                nans.append(np.nan)
            nones = pd.Series(nans, index=[0])
            audio_features = pd.DataFrame(nones, index=[0])
            continue
        
        # Concat the dfs
        track_df = pd.DataFrame(audio_features, index=[0])
        partion =  track_df[playlist_features_list]
        playlist_df = pd.concat([playlist_df, partion], axis = 0, ignore_index = True)
        
    return playlist_df

df_num = 0
max = 999000
low = 0
high = 999

auth_manager = SpotifyClientCredentials(client_id=credentials.SPOTIPY_CLIENT_ID, client_secret=credentials.SPOTIPY_CLIENT_SECRET)
sp = spotipy.Spotify(auth_manager=auth_manager)

lexicon = Empath()
lexicon.create_category("throwback", ["throwback"],model = "reddit")
lexicon.create_category("party", ["party","pregame"],model = "reddit")
lexicon.create_category("workout", ["workout","rap"],model = "reddit")

while low <= max:
    file_name = "data/mpd.slice." + str(low) + "-" + str(high) + ".json"
    f1 = open(file_name)
    data = json.load(f1)
    print("loaded " + file_name)
    

    for i in range(len(data['playlists'])):
        if low == 0 and i >= starter :
            # get the track ids
            playlist_tracks = []
            for j in range(len(data['playlists'][i]['tracks'])):
                song_id = data['playlists'][i]['tracks'][j]['track_uri']
                song_id = song_id.replace("spotify:track:", "")
                playlist_tracks.append(song_id)
            # Get the artisits
            playlist_artists = []
            for j in range(len(data['playlists'][i]['tracks'])):
                artist_id = data['playlists'][i]['tracks'][j]['artist_uri']
                artist_id = artist_id.replace("spotify:artist:", "")
                playlist_artists.append(artist_id)

            playlist_0 = analyze_playlist(playlist_tracks, sp)

            emotions_df = pd.DataFrame()
            for j in range(len(data['playlists'][i]['tracks'])):
                printer = str(i) + " - " + str(j)
                print(printer)
                track_name = data['playlists'][i]['tracks'][j]['track_name']
                artist_name = data['playlists'][i]['tracks'][j]['artist_name']
                try: 
                    song = genius.search_song(track_name, artist=artist_name, get_full_info = False)
                    if(song != None):
                        lyrics = song.lyrics

                        # Use the Empath object to analyze the text for different emotions
                        emotions = lexicon.analyze(lyrics, normalize=True)
                        emotions_df_song = pd.DataFrame(emotions, index=[0])

                        emotions_df = pd.concat([emotions_df, emotions_df_song], ignore_index = True)
                except requests.exceptions.Timeout:
                    cats = list(lexicon.cats.keys())
                    nans = []
                    for x in range(len(cats)):
                        nans.append(np.nan)
                    nones = pd.Series(nans, index=cats)
                    emotions_df_song = pd.DataFrame(nones, index=[0])
                    emotions_df = pd.concat([emotions_df, emotions_df_song], ignore_index = True)
                    continue
            
            playlist_data = pd.concat([emotions_df, playlist_0],axis=1, ignore_index = False)

            name = "df"+ str(df_num) + ".csv"
            directory = 'playlist_data'
            filename = os.path.join(directory, name)
            playlist_data.to_csv(filename, index=False)
            df_num = df_num + 1
        else:
            #print("skipped df" + str(i))
            df_num = df_num + 1
        
    low = low + 1000
    high = high + 1000


