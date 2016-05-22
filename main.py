import argparse
import datetime
import logging
import os
import sys
from time import sleep

import requests


SEARCH_URL = "http://interactive.movingimage.us/pu.php"
FILE_NAME_FORMAT_STRING = "%Y_%m_%d_%H_%M_%S_{:0>3}-0.mp4"
DOWNLOAD_URL = "http://interactive.movingimage.us/save_file.php"
DOWNLOAD_DICT = {
	'type': 'movie',
	'file': 'saved/animation/{0}'
}
DEBUG_OUT_FREQUENCY = 1
OUTPUT_DIRECTORY = 'output'

logging.basicConfig(stream=sys.stdout, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

# argparse stuff

def _make_second_block(dt):
	stub = datetime.date.strftime(dt, FILE_NAME_FORMAT_STRING)
	return [
		stub.format(i) for i in range(1000)
	]


def _contains_download(doc_text):
	return 'Oops!' not in doc_text


def _fetch_and_save_movie(movie_filename):
	log.info('Saving: ' + movie_filename)
	if not os.path.exists(OUTPUT_DIRECTORY):
		os.makedirs(OUTPUT_DIRECTORY)
	movie_fetch_args = dict(DOWNLOAD_DICT)
	movie_fetch_args['file'] = movie_fetch_args['file'].format(movie_filename)
	try:
		with open(OUTPUT_DIRECTORY + '/' + movie_filename, 'wb') as f:
			res = requests.get(DOWNLOAD_URL, params=movie_fetch_args, stream=True)
			if not res.ok:
				raise Exception('fetch failed')
			for block in res.iter_content(1024):
				f.write(block)
		log.info(movie_filename + ' saved successfully')
	except Exception as e:
		log.exception(movie_filename + ' save failed')


def main():
	START = datetime.datetime(year=2016, month=5, day=21, hour=18, minute=21, second=16)
	END = datetime.datetime(year=2016, month=5, day=21, hour=18, minute=21, second=17)
	INTERVAL = datetime.timedelta(seconds=1)

	cur = START
	while cur < END:
		if cur.second % DEBUG_OUT_FREQUENCY == 0:
			log.debug(cur)
		for movie_filename in _make_second_block(cur):
			res = requests.get(SEARCH_URL, params={'f': movie_filename})
			if res.status_code != requests.codes.ok:
				log.info("Bad request for {0}: {1}".format(movie_filename, res.status_code))
				sleep(5)
			if _contains_download(res.text):
				_fetch_and_save_movie(movie_filename)
		cur += INTERVAL


if __name__ == '__main__':
	main()