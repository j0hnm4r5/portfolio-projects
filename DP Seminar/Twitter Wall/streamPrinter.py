from twython import TwythonStreamer
from twitterCredentials import *

import re, os, sys

import urllib
from PIL import Image

import HTMLParser
from unidecode import unidecode

from ThermalPrinter import *


class TwitterStream(TwythonStreamer):

	def on_success(self, data):
		if 'text' in data:

			# IMAGE ------------------------------------------------------------------------------
			if 'entities' in data:
				entities = data['entities']
				if 'media' in entities:
					media = entities['media'][0]
					if 'media_url' in media:
						media_url = media['media_url']
						try:
							print "********* I FOUND AN IMAGE! **********"
							img_file = urllib.urlretrieve(media_url, r"images/" + media_url.split("/")[-1])[0]
							image = Image.open(img_file)
							original_width, original_height = image.size
							new_width = 384
							new_height = int((original_height * new_width) / original_width)
							image = image.resize((new_width, new_height), Image.ANTIALIAS)
							image = image.rotate(180)
							printer.printImage(image, True)
							os.remove(img_file)
							printer.feed(2)

						except:
							printer.feed(2)	
			
			# EXTRACT ----------------------------------------------------------------------------
			text = data['text'].encode('utf-8')
			username = data['user']['screen_name'].encode('utf-8')
			time_created = data['created_at'][:20] + data['created_at'][26:]

			print "@" + username + ": " + text

			splitter = re.compile(re.escape(keyword), re.IGNORECASE)


			# TEXT -------------------------------------------------------------------------------
			original_text = data['text']
			printable_text = unidecode(HTMLParser.HTMLParser().unescape(original_text))

			reversed_text = []
			for line in string_split(printable_text, 32):
				reversed_text.append(line.ljust(32))
			reversed_text.reverse()
			reversed_text = "".join(reversed_text)

			keyword_text = splitter.split(reversed_text)


			printer.upsideDownOn()
			i = 0
			while i < len(keyword_text) - 1:
				printer.thermal_print(keyword_text[i])
				printer.underlineOn()
				printer.thermal_print(keyword)
				printer.underlineOff()
				i += 1
			printer.thermal_print(keyword_text[-1])


			# TIME -------------------------------------------------------------------------------
			if 'created_at' in data:

				time_string = data['created_at']
				printer.writeBytes(174) # <<
				time_created = " " + time_string[4:10] + ", " + time_string[26:] + " at " + time_string[11:19] + " UTC "
				printer.thermal_print(time_created)
				printer.writeBytes(175) # >>
				printer.println()

			# USER -------------------------------------------------------------------------------
			printer.justify('R')
			printer.inverseOn()
			printer.boldOn()
			printer.thermal_print(" @" + data['user']['screen_name'] + " \n")
			printer.boldOff()
			printer.inverseOff()
			printer.justify('L')
			
			printer.upsideDownOff()

			printer.feed(2)


	def on_error(self, status_code, data):
		print status_code
		# self.disconnect()

def string_split(string, width):
	for start in range(0, len(string), width):
		yield string[start:start+width]

stream = TwitterStream(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
printer = ThermalPrinter("/dev/ttyAMA0", 19200, timeout=5)

keyword = sys.argv[1]
if keyword == "sample":
	stream.statuses.sample()
else:
	stream.statuses.filter(track=keyword)
