from bs4 import BeautifulSoup
import os
import requests

BASE_URL = "http://interactive.movingimage.us/saved/animation/"
BASE_URL = "http://interactive.movingimage.us/saved/flipbook/mp4/"
OUTPUT_DIRECTORY = 'crawl_output'

if not os.path.exists(OUTPUT_DIRECTORY):
	os.makedirs(OUTPUT_DIRECTORY)


soup = BeautifulSoup(requests.get(BASE_URL).content, 'html.parser')
for link in soup.findAll('a'):
	href = link.get('href')
	if href.startswith('2016'):
		with open(OUTPUT_DIRECTORY + '/flip' + href, 'wb') as f:
			res = requests.get(BASE_URL + href, stream=True)
			for block in res.iter_content(1024):
				f.write(block)
		print(href + ' written')
