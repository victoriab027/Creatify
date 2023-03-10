import requests
r = requests.post(
    "https://api.deepai.org/api/text2img",
    data={
        'text': 'Alt-Rock, Alternative, Chicago House',
    },
    headers={'api-key': 'quickstart-QUdJIGlzIGNvbWluZy4uLi4K'}
)
print(r.json())
# import spacy

# nlp = spacy.load("en_core_web_sm")

# text = "I love listening to Reggae and Hip Hop music"

# doc = nlp(text)

# for ent in doc.ents:
#     print(ent.text, ent.label_)
