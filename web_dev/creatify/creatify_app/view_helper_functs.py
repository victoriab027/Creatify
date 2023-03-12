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
    
    if 'Danceability' in slider['name']:
      if slider["Level"] <25:
        slider["Level"] = "Low"+ f" {slider['name']}"
      elif slider["Level"] <75:
        slider["Level"] = "Medium"+ f" {slider['name']}"
      elif slider['Level'] >= 75:
        slider["Level"] = "High"+ f" {slider['name']}"
    elif 'Energy' in slider['name']:
      if slider["Level"] <25:
        slider["Level"] = "Calm"+ f" {slider['name']}"
      elif slider["Level"] <75:
        slider["Level"] = "Average"+ f" {slider['name']}"
      elif slider['Level'] >= 75:
        slider["Level"] = "Energetic"
    elif 'Tempo' in slider['name']:
      if slider["Level"] <25:
        slider["Level"] = "Slower"+ f" {slider['name']}"
      elif slider["Level"] <75:
        slider["Level"] = "Average"+ f" {slider['name']}"
      elif slider['Level'] >= 75:
        slider["Level"] = "Faster"+ f" {slider['name']}"
    elif 'Instrumentalness' in slider['name']:
      if slider["Level"] <25:
        slider["Level"] = "Vocal"
      elif slider["Level"] <75:
        slider["Level"] = "Average"+ f" {slider['name']}"
      elif slider['Level'] >= 75:
        slider["Level"] = "Instrumental"
    elif 'Valence' in slider['name']:
      if slider["Level"] <25: #Meloncholic
        slider["Level"] = "Meloncholic"
      elif slider["Level"] <75:
        slider["Level"] = "Average"+ f" {slider['name']}"
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
      results = sp.current_user_top_tracks(time_range=sp_range, limit=50)
      for i in range(len(results)):
          top_tracks.append(results['items'][i]['uri'])
  audio_features = sp.audio_features(top_tracks)
  df = pd.DataFrame(audio_features)
  songs = {'danceability': [df.loc[df['danceability'].idxmin(), 'uri'], df.loc[df['danceability'].idxmax(), 'uri']], 
      'energy': [df.loc[df['energy'].idxmin(), 'uri'], df.loc[df['energy'].idxmax(), 'uri']], 
        'valence': [df.loc[df['valence'].idxmin(), 'uri'], df.loc[df['valence'].idxmax(), 'uri']],
        'instrumentalness': [df.loc[df['instrumentalness'].idxmin(), 'uri'], df.loc[df['instrumentalness'].idxmax(), 'uri']],
        'tempo': [df.loc[df['tempo'].idxmin(), 'uri'], df.loc[df['tempo'].idxmax(), 'uri']]}
  return songs # this returns the above values in min then max order

def generate_playlist(token,generes_list,settings, goal):
    '''
    This is the main function that will generate the playlist for the user. It contains queries to the Spotify API as well
    as the OpenAI GPT 3.5 AI which means it can take a second to run! It is ended by creating the playlist and using the 
    first name suggestion onto the users' spotify account. 

    Returns: the other suggested playlist titles as well as the id of the new playlist created

    Example call:


    settings = [{"Name": "danceability", "On": True, "Level": 1},
            {"Name": "energy", "On": True,"Level": 1},
            {"Name": "valence", "On": True,"Level": 0},
            {"Name": "loudness","On": False, "Level": 1},
            {"Name": "instrumentalness","On": False, "Level": -1},
            {"Name": "liveness", "On": True,"Level": 1}]

    settings_df = pd.DataFrame(settings)

    goal = 20
    generes_list = ["indie-pop","dancehall"]
    sp = get_logged_in()
    titles, i = generate_playlist(sp,generes_list,settings_df, goal)

    
    '''
    sp = spotipy.Spotify(auth=token)
    print('begin of generate playlist')
    settings_df = pd.DataFrame(settings)
    songs = gather_songs(sp,generes_list,settings_df, goal)
    print('gathered songs')
    input = "The playlist has the following songs:"
    for i in range(len(songs)) and i < 20:
        song_name = songs['track_name'][i]
        song_artist = songs['artist'][i] # only the first artist
        input = input + "\n- " +song_name + " by " + song_artist
    openai.api_key = credentials.api_key
    output = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
                {"role": "system", "content": "You are a playlist reccomendation software. The user will ask for a playlist title given a list of songs in the playlist."},
                {"role": "user", "content": input},
                {"role": "assistant", "content": "A playlist title should not be longer than 7 words and at minimum 2 words"},
                {"role": "assistant", "content": "Give more than 1 suggestion"}
            ]
        ) 
    reccomendation = output['choices'][0]['message']['content']
    print('reccc',reccomendation)
    bullet_points = reccomendation.split('\n\n')[1].split('\n')[0:]
    playlist_titles = [point[2:] for point in bullet_points]
    best_title = playlist_titles[0]

    username = sp.current_user()['id']
    result = sp.user_playlist_create(username, name=best_title)
    playlist_id = result['id']

    logger = logging.getLogger('examples.add_tracks_to_playlist')
    logging.basicConfig(level='DEBUG')
    scope = 'playlist-modify-public'

    tracks = songs["track_id"]

    sp.user_playlist_add_tracks(username, playlist_id=playlist_id, tracks=tracks)
    print('right before return')
    return playlist_titles, playlist_id



#############################


# HELPER FUNCTIONS


############################
def find_and_filter(settings, genres_list, sp):
    #FINDING
    search = ''
    for i in range(len(genres_list)):
      search += 'genre:'
      search +=  f'"{genres_list[i]}"'
      if genres_list[i] != genres_list[-1]:
        search += ' OR '
    
    print(search)
      
    results = sp.search(q = search, type = 'track', limit=50, offset = 0)
    song_features_list = ["artist","album","track_name",  "track_id","Danceability","Energy","Key","Loudness","mode", "Speechiness","Instrumentalness","Liveness","Valence","Tempo", "duration_ms","time_signature"]
    song_df = pd.DataFrame(columns = song_features_list)
    tracks = results["tracks"]
    print("tracks")
    print(tracks)
    for track in tracks:
        # Create empty dict
        print(track)
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
        print("track_df")
        print(track_df)
    #FILTERING
    num_false = settings["On"].value_counts().loc[False]
    if num_false == 5:
      song_df = song_df.head(50)
    else:
      for index, setting in settings.iterrows():
          if setting["On"]:
                  print(int(setting["Level"]))
                  level = int(setting["Level"])/50 
                  var = song_df[setting["Name"]].var()
                  song_df = song_df[(song_df[setting["Name"]] >= level*song_df[setting["Name"]].mean()-2*var) & (song_df[setting["Name"]] <= level*song_df[setting["Name"]].mean()+2*var)]
      
    return song_df

def gather_songs(sp, generes_list, settings_df, goal):
    final_df = find_and_filter(settings_df,generes_list,sp)
    print("goal: ")
    print(goal)
    print("final_df")
    print(len(final_df))
    print(final_df)
    while (len(final_df) < goal):
        getter = find_and_filter(settings_df,generes_list,sp)
        final_df = pd.concat([final_df, getter], ignore_index = True)
    return final_df
