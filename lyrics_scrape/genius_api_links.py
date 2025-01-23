from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import requests
import re
import time

billboard_songs = pd.read_csv('/Users/sberry5/Documents/teaching/all_billboard_songs.csv')

billboard_songs['artist'] = billboard_songs['artist'].str.replace(r'\n|\t', '', regex=True)

billboard_songs['artist'] = billboard_songs['artist'].str.replace(r' [Ff]eaturing.*', '', regex=True)

billboard_songs['artist'] = billboard_songs['artist'].str.replace(r"\[.*?'\]", '', regex=True)

billboard_songs['artist'] = billboard_songs['artist'].str.replace(r'^\s+|\s+$', '', regex=True)

billboard_songs['artist'] = billboard_songs['artist'].str.replace(r'\s{2,}', ' ', regex=True)

billboard_songs['song'] = billboard_songs['song'].str.replace(r'\n|\t', '', regex=True)

billboard_songs['song'] = billboard_songs['song'].str.replace(r'\(.*?\)', '', regex=True)

billboard_songs['song'] = billboard_songs['song'].str.replace(r"\[.*?'\]", '', regex=True)

billboard_songs['song'] = billboard_songs['song'].str.replace(r'^\s+|\s+$', '', regex=True)

billboard_songs['song'] = billboard_songs['song'].str.replace(r'\s{2,}', ' ', regex=True)

billboard_songs['search_artist'] = billboard_songs['artist'].str.lower()

billboard_songs['search_artist'] = billboard_songs['search_artist'].str.replace(r' ', '%20', regex=True)

billboard_songs['search_song'] = billboard_songs['song'].str.lower()

billboard_songs['search_song'] = billboard_songs['search_song'].str.replace(r' ', '%20', regex=True)

billboard_songs['query'] = billboard_songs['search_artist'] + '%20' + billboard_songs['search_song']

billboard_songs['query'] = billboard_songs['query'].str.replace(r'&', 'and', regex=True)

billboard_songs['query'] = billboard_songs['query'].str.replace(r'%20{2,}', '%20', regex=True)

search_query = billboard_songs['query'].drop_duplicates()

search_query['genius_link'] = 'https://api.genius.com/search?q=' + search_query


id = 'S6MtzxA7RXPxQiLNAuATCTv9VQ3k17nuAXQWkt_txCR7N2pZwpoKVde-FPbMRFE9'
secret = 'vIo1zdRRWxX16A8N6EskD52Hcz0DP8KmFeKqkY32oMediLjC-pUiHYoILQx-TeUb'    
headers = {'Authorization': 'Bearer ' + secret}

def get_genius_link(link):
    time.sleep(np.random.uniform(.1, .5, 1)[0])
    try:
        req_json = requests.get(link, headers=headers).json()
        song_id = req_json['response']['hits'][0]['result']['id']
        returned_song = req_json['response']['hits'][0]['result']['title']
        returned_artist = req_json['response']['hits'][0]['result']['primary_artist']['name']
        song_link = 'https://api.genius.com/' + 'songs/' + str(song_id)
        req_json = requests.get(song_link, headers=headers).json()
        lyrics_link = req_json['response']['song']['url']
        result = pd.DataFrame({'song': returned_song, 
                               'artist': returned_artist, 
                               'lyrics_link': lyrics_link, 
                               'query': link}, index=[0])
        return result
    except:
        return pd.DataFrame({'song': None, 
                               'artist': None, 
                               'lyrics_link': None, 
                               'query': link}, index=[0])
    

get_genius_link(search_query['genius_link'][10])


genius_links = []

for link in search_query['genius_link'][0:10]:
    genius_links.append(get_genius_link(link))

all_genius_links = pd.concat(genius_links)

all_genius_links.to_csv('/Users/sberry5/Documents/teaching/all_genius_links.csv', index=False)

# scp genius_api_links.py sberry5@crcfe02.crc.nd.edu:/afs/crc.nd.edu/user/s/sberry5/billboard_scrape/
# scp sberry5@crcfe02.crc.nd.edu:/afs/crc.nd.edu/user/s/sberry5/billboard_scrape/all_billboard_songs.csv Documents/

#req_json = requests.get(search_link, headers=headers).json()

#song_id = req_json['response']['hits'][0]['result']['id']
#returned_song = req_json['response']['hits'][0]['result']['title']
#returned_artist = req_json['response']['hits'][0]['result']['primary_artist']['name']

#song_link = 'https://api.genius.com/' + 'songs/' + str(song_id)

#req_json = requests.get(song_link, headers=headers).json()

#lyrics_link = req_json['response']['song']['url']

#lyrics = requests.get(lyrics_link)

#lyric_soup = BeautifulSoup(lyrics.text, 'html.parser')

#lyrics_return = lyric_soup.select('#lyrics-root-pin-spacer')

#lyrics_return = lyrics_return[0].get_text()

#lyrics_return = re.sub(r'([a-z])([A-Z])', '\\1 \\2', lyrics_return)

#lyrics_return = re.sub(r'\[.*?\]', ' ', lyrics_return)

#lyrics_return = re.sub(r'^.*Lyrics ', '', lyrics_return)