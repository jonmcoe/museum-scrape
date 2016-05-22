import argparse
import datetime
import requests
from time import sleep


SEARCH_URL = "http://interactive.movingimage.us/pu.php"
FILE_NAME_FORMAT_STRING = "%Y_%m_%d_%H_%M_%S_{:0>3}-0.mp4"
DOWNLOAD_URL = "http://interactive.movingimage.us/save_file.php"
DOWNLOAD_DICT = {
	'type': 'movie',
	'file': 'saved/animation/{0}'
}
DEBUG_OUT_FREQUENCY = 1

# argparse stuff

def _make_second_block(dt):
	stub = datetime.date.strftime(dt, FILE_NAME_FORMAT_STRING)
	return [
		stub.format(i) for i in range(1000)
	]


def _contains_download(doc_text):
	return 'Oops!' not in doc_text


def _fetch_and_save_movie(movie_filename):
	print(movie_filename)
	# request, local file write
	return


def main():
	START = datetime.datetime(year=2016, month=5, day=21, hour=18, minute=21, second=15)
	END = datetime.datetime(year=2016, month=5, day=21, hour=18, minute=21, second=17)
	INTERVAL = datetime.timedelta(seconds=1)

	cur = START
	while cur < END:
		if cur.second % DEBUG_OUT_FREQUENCY == 0:
			print(cur)
		for movie_filename in _make_second_block(cur):
			res = requests.get(SEARCH_URL, params={'f': movie_filename})
			if res.status_code != requests.codes.ok:
				print("Bad request for {0}: {1}".format(movie_filename, res.status_code))
				sleep(5)
			if _contains_download(res.text):
				_fetch_and_save_movie(movie_filename)
		cur += INTERVAL


if __name__ == '__main__':
	main()