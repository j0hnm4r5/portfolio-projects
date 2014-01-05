from twython import TwythonStreamer
from twitterCredentials import *
import urllib
import os, sys
from PIL import Image
# import pprint


class MyStreamer(TwythonStreamer):

	def on_success(self, data):
		# pprint.pprint(data)

		if 'text' in data:
			print data['text'].encode('utf-8')

		if 'entities' in data:
			entities = data['entities']
			if 'urls' in entities:
				urls = entities['urls']
				for link in urls:
					url = link['expanded_url']					
					for filetype in filetypes:
						index = url.find(filetype, -5)
						if index > 0:
							if 'text' in data:
								print "********* I FOUND AN IMAGE! **********"
								text = data['text'].encode('utf-8')
							if 'user' in data:
								if 'screen_name' in data['user']:
									username = data['user']['screen_name'].encode('utf-8')

							img = urllib.urlretrieve(url, r"/Users/johnmars/Documents/Fall 2013/DP Seminar/SpaceGrabImages/" + url.split("/")[-1])[0]
							try:
								im = Image.open(img)
								im.thumbnail(size, Image.ANTIALIAS)
								im.save(img)
							except IOError:
								print "cannot create thumbnail for '%s'" % img

							with open(r'/Users/johnmars/Documents/Fall 2013/DP Seminar/spaceGrab.txt', 'a') as f:

								f.write("\n@" + username + " tweeted " + text + " ||| Here's the image: " + img[62:])


	def on_error(self, status_code, data):
		print status_code
		# self.disconnect()

stream = MyStreamer(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

filetypes = [".jpg", ".png", ".gif", ".jpeg", ".tiff", ".bmp", ".webp"]
size = 512, 512

stream.statuses.filter(track='outer space, architecture')