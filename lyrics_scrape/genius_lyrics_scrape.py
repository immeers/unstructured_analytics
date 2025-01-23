from bs4 import BeautifulSoup
from joblib import Parallel, delayed
import numpy as np
import pandas as pd
import re
import requests
import time

genius_links = pd.read_csv('/Users/sberry5/Documents/all_genius_links.csv')

genius_links = genius_links.dropna()

headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:126.0) Gecko/20100101 Firefox/126.0', 
         'Host': 'genius.com'}

proxies = {
    'https':'https://44.195.247.145:80'
}

def lyric_getter(url):
    try:
        time.sleep(np.random.uniform(.5, 1, 1)[0])
        lyrics = requests.get(url, headers=headers)
        if lyrics.status_code != 200:
            print("status code error: " + url)
            return
        lyric_soup = BeautifulSoup(lyrics.text, 'html.parser')
        lyrics_return = lyric_soup.select('#lyrics-root-pin-spacer')
        lyrics_return = lyrics_return[0].get_text()
        lyrics_return = re.sub(r'([a-z])([A-Z])', '\\1 \\2', lyrics_return)
        lyrics_return = re.sub(r'\[.*?\]', ' ', lyrics_return)
        lyrics_return = re.sub(r'^.*Lyrics ', '', lyrics_return)
        return lyrics_return
    except:
        return None

result = Parallel(n_jobs=14)(delayed(lyric_getter)(x) for x in genius_links['lyrics_link'])

result2 = Parallel(n_jobs=14)(delayed(lyric_getter)(x) for x in genius_links['lyrics_link'][62923:64685])

# now we can put result and result_2 together into a Series
result = result.extend(result2)

result_series = pd.Series(result)

genius_links['lyrics'] = result_series  

genius_links['lyrics'].isna().sum()

genius_links.to_csv('/Users/sberry5/Documents/all_genius_lyrics.csv', index=False)

test = pd.read_csv('/Users/sberry5/Documents/all_genius_lyrics.csv')
test['lyrics'].isna().sum()
test.loc[62923:64684]

test.to_csv('/Users/sberry5/Documents/all_genius_lyrics.csv', index=False)

len(result2)
result = test['lyrics'].to_list()
extend_test = result_test.extend(result2)
test_series = pd.Series(result_test)
test_series
lyric_getter('https://genius.com/Brns-past-lives-lyrics')