# Creatify
The goal of this project is to create new spotify playlists based on user-selected criteria. The users select genres they want and then can manipulate certain psychoacusotic values such as "Danceability" and "Instrumentalness". Then Creatify generates a playlist following this criterion for the user. The model used for playlist generation was developed on Jupyter notebooks included in the repo and then implemented as a python script trained on data gathered from the Spotify API. The web application was created with Django.

## NLP
DESCRIPTION OF THE NLP portion

Many thanks to Ethan Fast's [<i>Empath</i> client](https://github.com/Ejhfast/empath-client) for making this possible.


### Project Organization

    ├── README.md          <- The top-level README for developers using this project.
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    │
    └── web_dev            <- Source code for website implementation


<p><small>Project formatting based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
