import asyncio
import aiohttp
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
import random
import re

import credentials

async def get_audio_features(track_id, token):
    """Get audio features for a track from Spotify API."""
    headers = {
        'Authorization': f'Bearer {token}'
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://api.spotify.com/v1/tracks/{track_id}', headers=headers) as response:
            if response.status == 200:
                return await response.json()
            else:
                return None

async def main(track_ids, token):
    # Create tasks for each track ID
    tasks = [get_audio_features(track_id, token) for track_id in track_ids]

    # Fetch audio features asynchronously
    audio_features = await asyncio.gather(*tasks)

    return audio_features



## THE CODE
# Gain access to mainupation
SCOPE = ('user-read-recently-played,user-library-read,playlist-modify-private,playlist-modify-public,user-modify-playback-state,user-read-playback-state')
sp_oauth = oauth2.SpotifyOAuth(credentials.SPOTIPY_CLIENT_ID,credentials.SPOTIPY_CLIENT_SECRET, credentials.SPOTIPY_REDIRECT_URI ,scope=SCOPE )
print(sp_oauth)
#click "Accept" in your browser when the auth window pops up
code = sp_oauth.get_auth_response(open_browser=True)
print(code)
token = sp_oauth.get_access_token(code)
refresh_token = token['refresh_token']
sp = spotipy.Spotify(auth=token['access_token'])
username = sp.current_user()['id']


genres_list = ['country', 'pop', 'summer']
settings = [{'Name': 'danceability', 'On': True, 'Level': 67}, {'Name': 'energy', 'On': True, 'Level': 89}, {'Name': 'valence', 'On': True, 'Level': 82}, {'Name': 'instrumentalness', 'On': False, 'Level': 0}, {'Name': 'tempo', 'On': True, 'Level': 77}]
settings = pd.DataFrame(settings)
goal = 15

#FINDING
# Generate a list of 10 track IDs for each genre
track_ids = [track['id'] for genre in genres_list for track in sp.search(q='genre:' + genre, type='track', limit=10)['tracks']['items']]

# Shuffle the list of track IDs
random.shuffle(track_ids)

# Generate recommendations based on the shuffled track IDs
tracks = [track for i in range(0, len(track_ids), 5) for track in sp.recommendations(seed_genre=genres_list, seed_tracks=track_ids[i:i+5], limit=100)['tracks']]
track_ids = []
for track in tracks:
    track_ids.append(track['id'])
print("got reccomendations")
print(len(tracks))

song_features_list = ["artist","album","track_name",  "track_id","danceability","energy","key","loudness","mode", "speechiness","instrumentalness","liveness","valence","tempo", "duration_ms","time_signature"]
song_df = pd.DataFrame(columns = song_features_list)

# Run the event loop and get the audio features
audio_features = asyncio.run(main(track_ids, token))
print(len(song_df))
print(len(audio_features))

# Process the results
# for track_id, features in zip(track_ids, audio_features):
#     if features:
#         print(f'Audio features for track ID {track_id}: {features}')
#     else:
#        # print(f'Failed to fetch audio features for track ID {track_id}')
#        continue


