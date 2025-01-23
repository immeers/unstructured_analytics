from bs4 import BeautifulSoup
import numpy as np
import re
import requests
import time
def lyric_getter(url):
    try:
        time.sleep(np.random.uniform(.1, .3, 1)[0])
        lyrics = requests.get(url)
        lyric_soup = BeautifulSoup(lyrics.text, 'html.parser')
        lyrics_return = lyric_soup.select('#lyrics-root-pin-spacer')
        lyrics_return = lyrics_return[0].get_text()
        lyrics_return = re.sub(r'([a-z])([A-Z])', '\\1 \\2', lyrics_return)
        lyrics_return = re.sub(r'\[.*?\]', ' ', lyrics_return)
        lyrics_return = re.sub(r'^.*Lyrics ', '', lyrics_return)
        return lyrics_return
    except:
        return None