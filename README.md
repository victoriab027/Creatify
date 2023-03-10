# Creatify
Creatify is designed for music lovers who want to discover new songs within their preferred genres. It enables users to create a randomly generated based on their preferences, allowing them to broaden their music discovery experience within Spotify.<br>

Once users are logged in with their Spotify account, they are prompted to select their preferred target genres for the new playlist. These genres are all Spotify created genres ranging from “Disney” to “German”. Users can then toggle on or off audio features such as danceability, tempo, and energy to be high, low or average. In order to increase understanding of what these audio features are, we have a web player corresponding to each audio feature toggle. These web players are individualized for each user as it pulls from their most recent listened to tracks. It allows users to not only read what danceability is but also hear it in their own specific taste in music.Finally, the user can specify the minimum number of songs they would like in the playlist.<br>

Once the parameters are set, songs are then randomly gathered from Spotify that fall within the target genres and their audio features are compared to the average audio features of the other songs in the query results. If found to be within the goal features, they are added straight to the new playlist. The randomization of this playlist generation is unique since it allows users to listen to songs that might not normally be recommended but still fall within what they wish to discover in music, giving them a unique listening experience. <br>

After the playlist is created, Creatify queries the OpenAI API to generate a custom playlist name based on the playlist's characteristics.<br>

Creatify is designed for Spotify lovers who are eager to discover new music. It enables users to create a custom playlist that is randomly generated based on their preferences and even comes with a custom playlist name. The integrates with Spotify is easy as it adds the playlist to straight their account where they can go enjoy their newly discovered music.

## Project Organization

    ├── README.md          <- The top-level README for developers the project.
    │
    ├── notebooks          <- Exploration of the project through jupyter notebooks. 
    │                         Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`. These were used for discover about 
    │                         the APIs and how the application would work
    │
    ├── python_scripts     <- Where the jupter notebooks become functions and scripts to be implemented
    │                        into the django project
    │
    └── web_dev            <- Source code for website implementation in django
      ├── creatify
      │ ├── creatify       <- Stores the pyton scripts required for the django project such as urls.py
      │ │
      │ └── creaitfy_app
      │   ├── static       <- Contains the pages' .css and .js files
      │   │
      │   └── templates    <- Contains the html files for each page
      └── playground


## Notes
In order to run the script to generate your own playlists, you will need a credentials.py file in the following format:

SPOTIPY_CLIENT_ID = "SPOTIFY_CLIENT_ID"<br>
SPOTIPY_CLIENT_SECRET = "SPOTIFY_CLIENT_SECRET"<br>
SPOTIPY_REDIRECT_URI =  "SPOTIFY_REDIRECT_URI"<br>
api_key = "OPEN_AI_API_KEY"

## Formatting
<p><small>Project formatting based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
