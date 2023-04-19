import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import argparse
import logging
import pandas as pd
import numpy as np
import requests
from spotipy import oauth2
import re
import os
import openai
from . import credentials
import random

''' 

TO RUN:

3. You should run: generate_playlist(sp,generes_list,settings_df, goal)
  a. sp is the spotify thing
  b. genres_list is a list of the clicked genres
  c. settings_df is the dataframe we've discussed. Now the values should be 0 -> 100
  d. goal is the number of minimum songs
4. This function will return the other suggested playlist titles as a list as well as the id of the new playlist created
  a. I will need both of these variables for the results page


'''

def convert_slider_vals(slider_list):
  for slider in slider_list:
    if not slider['On']:
      slider["Level"] = "skip"
      continue
    
    if 'danceability' in slider['Name']:
      if slider["Level"] <25:
        slider["Level"] = "Low"+ f" {slider['Name']}"
      elif slider["Level"] <75:
        slider["Level"] = "Medium"+ f" {slider['Name']}"
      elif slider['Level'] >= 75:
        slider["Level"] = "High"+ f" {slider['Name']}"
    elif 'energy' in slider['Name']:
      if slider["Level"] <25:
        slider["Level"] = "Calm"+ f" {slider['Name']}"
      elif slider["Level"] <75:
        slider["Level"] = "Average"+ f" {slider['Name']}"
      elif slider['Level'] >= 75:
        slider["Level"] = "Energetic"
    elif 'tempo' in slider['Name']:
      if slider["Level"] <25:
        slider["Level"] = "Slower"+ f" {slider['Name']}"
      elif slider["Level"] <75:
        slider["Level"] = "Average"+ f" {slider['Name']}"
      elif slider['Level'] >= 75:
        slider["Level"] = "Faster"+ f" {slider['Name']}"
    elif 'instrumentalness' in slider['Name']:
      if slider["Level"] <25:
        slider["Level"] = "Vocal"
      elif slider["Level"] <75:
        slider["Level"] = "Average"+ f" {slider['Name']}"
      elif slider['Level'] >= 75:
        slider["Level"] = "Instrumental"
    elif 'valence' in slider['Name']:
      if slider["Level"] <25: #Meloncholic
        slider["Level"] = "Meloncholic"
      elif slider["Level"] <75:
        slider["Level"] = "Average"+ f" {slider['Name']}"
      elif slider['Level'] >= 75:
        slider["Level"] = "Cheery"
  return slider_list

def get_top_features(token): # fix so it can take a token instead
  '''
  This is a function that
  '''
  sp = spotipy.Spotify(auth=token)
  ranges = ['short_term', 'medium_term', 'long_term']
  top_tracks = []
  for sp_range in ranges:
    offset = 0
    while offset < 27:
        results = sp.current_user_top_tracks(time_range=sp_range, limit=50, offset = offset)
        for i in range(len(results)):
            top_tracks.append(results['items'][i]['uri'])
        offset += 7
  audio_features = sp.audio_features(top_tracks)
  df = pd.DataFrame(audio_features)
  songs = {'danceability': [df.loc[df['danceability'].idxmin(), 'uri'], df.loc[df['danceability'].idxmax(), 'uri']], 
      'energy': [df.loc[df['energy'].idxmin(), 'uri'], df.loc[df['energy'].idxmax(), 'uri']], 
        'valence': [df.loc[df['valence'].idxmin(), 'uri'], df.loc[df['valence'].idxmax(), 'uri']],
        'instrumentalness': [df.loc[df['instrumentalness'].idxmin(), 'uri'], df.loc[df['instrumentalness'].idxmax(), 'uri']],
        'tempo': [df.loc[df['tempo'].idxmin(), 'uri'], df.loc[df['tempo'].idxmax(), 'uri']]}
  return songs # this returns the above values in min then max order

def generate_playlist(token,generes_list,settings, goal):
    sp = spotipy.Spotify(auth=token)
    print('begin of generate playlist')
    settings_df = pd.DataFrame(settings)
    songs = gather_songs(sp,generes_list,settings_df, goal)
    # ADD ENGLISH CODE RIGHT HERE
    # REMINDER IT SHOULD ONLY RUN IF THE BAR IS DIABLBBED.
    # MIGHT BE EASIEST TO JUST PASS IN ANOTHER VAIRABLE THAT'S FALSE IF WE DON'T WANT ENGLISH OR SMTH
    print('gathered songs')

    # Shuffle the dataframe 
    songs = songs.iloc[np.random.permutation(len(songs))].reset_index(drop=True)
    input = "The playlist has the following songs:"
    i = 0
    while i in range(len(songs)) and i < 20:
        song_name = songs['track_name'][i]
        song_artist = songs['artist'][i] # only the first artist
        input = input + "\n- " +song_name + " by " + song_artist
        i += 1
    openai.api_key = credentials.api_key
    output = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
                {"role": "system", "content": "You are a playlist reccomendation software. The user will ask for a playlist title given a list of songs in the playlist."},
                {"role": "user", "content": input},
                {"role": "assistant", "content": "A playlist title should not be longer than 7 words and at minimum 2 words"},
                {"role": "assistant", "content": "Give more than 3 suggestions and less than 8"},
                {"role": "assistant", "content": "Structure your format in the output. ' here are three suggestions for playlist titles based on the songs you provided:\n1.Reccomendation\n2.Reccomendation\n3.Reccomendation\n4.Reccomendation\n5.Reccomendation, and so on'"}
            ]
        ) 
    reccomendation = output['choices'][0]['message']['content']
    print(reccomendation)
    #print('reccc',reccomendation)
    bullet_points = reccomendation.split('\n\n')[0].split('\n')[0:]
    playlist_titles = [point[2:] for point in bullet_points]
    playlist_titles = playlist_titles[1:]
    print(playlist_titles)
    best_title = playlist_titles[0]

    username = sp.current_user()['id']
    result = sp.user_playlist_create(username, name=best_title, description="A personalized discovery playlist created with Creatify")
    playlist_id = result['id']

    logger = logging.getLogger('examples.add_tracks_to_playlist')
    logging.basicConfig(level='DEBUG')
    scope = 'playlist-modify-public'

    tracks = songs["track_id"]

    sp.user_playlist_add_tracks(username, playlist_id=playlist_id, tracks=tracks)
    return playlist_titles, playlist_id



#############################


# HELPER FUNCTIONS


############################
def find_and_filter(settings, genres_list, sp):
    #FINDING
    # Generate a list of 10 track IDs for each genre
    track_ids = [track['id'] for genre in genres_list for track in sp.search(q='genre:' + genre, type='track', limit=10)['tracks']['items']]

    # Shuffle the list of track IDs
    random.shuffle(track_ids)

    # Generate recommendations based on the shuffled track IDs
    tracks = [track for i in range(0, len(track_ids), 5) for track in sp.recommendations(seed_genre=genres_list, seed_tracks=track_ids[i:i+5], limit=100)['tracks']]
    track_ids = []
    for track in tracks:
        track_ids.append(track['uri'])
    print("got reccomendations")
    print(len(tracks))

    song_features_list = ["artist","album","track_name",  "track_id","danceability","energy","key","loudness","mode", "speechiness","instrumentalness","liveness","valence","tempo", "duration_ms","time_signature"]
    song_df = pd.DataFrame(columns = song_features_list, index=range(len(track_ids)))

    # Fill all cells with NaN
    song_df[:] = float('nan')

    # Create empty dict
    playlist_features = {}
    playlist_features["artist"] = []
    playlist_features["album"] = []
    playlist_features["track_name"] = []
    playlist_features["track_id"] = []
    print('here 1')

    for i in range(len(track_ids)):  
        #song_df["artist"][i] = tracks[i]["album"]["artists"][0]["name"]
        playlist_features["artist"].append(tracks[i]["album"]["artists"][0]["name"])
        playlist_features["album"].append(tracks[i]["album"]["name"])
        playlist_features["track_name"].append(tracks[i]["name"])
        playlist_features["track_id"].append(tracks[i]["id"])
    print('here 2')
    song_df["artist"] =  playlist_features["artist"]
    song_df["album"] =  playlist_features["album"]
    song_df["track_name"] =  playlist_features["track_name"]
    song_df["track_id"] =  playlist_features["track_id"]
    print('here 3')
    for i in range(0, len(track_ids), 100):  
        audio_features = sp.audio_features(track_ids[i:i+100])# Batch size of 100 for API requests
        for j in range(len(audio_features)):
            # Update the dataframe with information from the dictionary for the specific track_id
            track_id = audio_features[j]["id"]
            dict_info = {}
            for feature in song_features_list[4:]:
                dict_info[feature] = audio_features[j][feature]
            for key, value in dict_info.items():
                song_df.loc[song_df['track_id'] == track_id, key] = value
    #FILTERING
    for index, setting in settings.iterrows():
        if setting["On"]:
            level = int(setting["Level"])/50 
            var = 0.1
            mean_1 = 0.5
            mean_2 = song_df[setting["Name"]].mean()
            if setting["Name"] == "tempo":
                mean_1 = 90 # kinda just guessing on this one
                var = song_df[setting["Name"]].var()
                song_df_1 = song_df[(song_df[setting["Name"]] >= level*mean_1-3*var) & (song_df[setting["Name"]] <= level*mean_1+3*var)]
                song_df_2 = song_df[(song_df[setting["Name"]] >= level*mean_2-3*var) & (song_df[setting["Name"]] <= level*mean_2+3*var)]
            else:
              song_df_1 = song_df[(song_df[setting["Name"]] >= level*mean_1-1.5*var) & (song_df[setting["Name"]] <= level*mean_1+1.5*var)]
              song_df_2 = song_df[(song_df[setting["Name"]] >= level*mean_2-1.5*var) & (song_df[setting["Name"]] <= level*mean_2+1.5*var)]
            song_df =  pd.concat([song_df_1, song_df_2], ignore_index = True)
    song_df.drop_duplicates(keep='first', inplace =  True)
    print(len(song_df))
    print('here 226')
    print("found "+str(len(song_df)))
    return song_df

def gather_songs(sp, generes_list, settings_df, goal):
    song_features_list = ["artist","album","track_name",  "track_id","danceability","energy","key","loudness","mode", "speechiness","instrumentalness","liveness","valence","tempo", "duration_ms","time_signature"]
    song_df = pd.DataFrame(columns = song_features_list)
    final_df = find_and_filter(settings_df,generes_list,sp)
    while (len(final_df) < goal):
        print("Still under. At length : ")
        print(len(final_df))
        getter = find_and_filter(settings_df,generes_list,sp)
        final_df = pd.concat([final_df, getter], ignore_index = True)
        final_df.drop_duplicates(keep='first', inplace =  True)
    if len(final_df) > 100:
      final_df = final_df[:100]
    return final_df