from twython import TwythonStreamer, Twython
from twitterCredentials import *

import time
import pprint


class MyStreamer(TwythonStreamer):

	def on_success(self, data):
		global start_mins
		mins = int(time.time() / 60)
		if 'text' in data:
			print data['text']
			print mins - start_mins
		if mins - start_mins != 0:
			start_mins = mins
			self.disconnect()

stream = MyStreamer(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

while True:
	current_trend = twitter.get_place_trends(id=23424977
)[0]['trends'][0]['name']
	start_mins = int(time.time() / 60)
	print "**************************************** " + current_trend + " *********"
	stream.statuses.filter(track=current_trend)
