import requests, re
from urlparse import urljoin
from bs4 import BeautifulSoup
from nltk.tokenize import RegexpTokenizer
from itertools import chain
from random import sample


BASE_URL = "http://genius.com"

def get_lyrics(artist):
	artist_url = "http://genius.com/artists/{}/".format(artist)
	r = requests.get(artist_url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36'})
	soup = BeautifulSoup(r.text)
	all_lyrics = []
	for s in soup.select('ul.song_list > li > a'):
		l = urljoin(BASE_URL, s['href'])
		r = requests.get(l)
		soup = BeautifulSoup(r.text)
		lyrics = soup.find('div', class_='lyrics').text.strip()
		all_lyrics.append(lyrics)
	return all_lyrics

def make_url_from(song_list):
	tokenizer = RegexpTokenizer(r'\w+')
	tokens = list(chain(*[tokenizer.tokenize(s) for s in song_list]))
	three = sample(tokens, 3)
	url_words = three[0].lower() + three[1].lower() + three[2].lower()
	return url_words

def validate(url): #adds http:// to www.whatever.com for redirecting
	p = re.compile(r'^https?://', re.IGNORECASE)
	if not re.findall(p, url):
		url = "http://" + url
		return url
	return url
