from bs4 import BeautifulSoup
import requests
import json

def crawl_lyrics(word):
    url = 'https://www.rappad.co/songs-about/'+word

    req = requests.get(url)
    soup = BeautifulSoup(req.text, "lxml")
    lyrics = soup.findAll("div", {"class": "lyrics"})[0]
    page = lyrics.findAll('p')

    return list(map(lambda web_element: web_element.text, page))