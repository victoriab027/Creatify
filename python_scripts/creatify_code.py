import pandas as pd

def get_top_features(sp):
    '''
    This is a function that
    '''

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