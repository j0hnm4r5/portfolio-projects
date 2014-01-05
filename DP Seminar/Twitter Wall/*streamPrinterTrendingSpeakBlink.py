from twython import TwythonStreamer, Twython
from twitterCredentials import *
import requests
import pygame
import re, os, sys, time
import urllib
from PIL import Image
import HTMLParser
import binascii
import RPi.GPIO as GPIO
from unidecode import unidecode
from ThermalPrinter import *


class TwitterStream(TwythonStreamer):

	def on_success(self, data):
		global LANGUAGES
		global start_mins
		mins = int(time.time() / 60)
		if mins - 1 - start_mins > 0:
			start_mins = mins
			self.disconnect()
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
			speak = text
			if "#" in data['text']:
				speak = text.replace('#', ' hashtag ')
			username = data['user']['screen_name'].encode('utf-8')
			time_created = data['created_at'][:20] + data['created_at'][26:]
			print "@" + username + ": " + text

			splitter = re.compile(re.escape(current_trend), re.IGNORECASE)


			# TWEET ------------------------------------------------------------------------------
			original_text = data['text']
			printable_text = unidecode(HTMLParser.HTMLParser().unescape(original_text))

			reversed_text = []
			for line in string_split(printable_text, 32):
				reversed_text.append(line.ljust(32))
			reversed_text.reverse()
			reversed_text = "".join(reversed_text)

			current_trend_text = splitter.split(reversed_text)


			printer.upsideDownOn()
			i = 0
			while i < len(current_trend_text) - 1:
				printer.thermal_print(current_trend_text[i])
				printer.underlineOn()
				printer.thermal_print(current_trend)
				printer.underlineOff()
				i += 1
			printer.thermal_print(current_trend_text[-1])


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

			printer.feed(1)

			# SPEAK ------------------------------------------------------------------------------
			params = {'key' : "6cfd2e1aca4a425dbdd9b427d52a3b21", 'hl' : "en-us", 'r' : "2", 'c' : "WAV"}
			params['src'] = speak
			if 'lang' in data:
				if data['lang'] in LANGUAGES:
					params['hl'] = LANGUAGES.get(data['lang'])
			r = requests.get('http://api.voicerss.org/', params=params)
			with open('tts.wav', 'wb') as f:
				f.write(r.content)
			pygame.mixer.music.load('tts.wav')
			pygame.mixer.music.play()
			while pygame.mixer.music.get_busy():
				clock.tick(1)
			os.remove('tts.wav')

			# BLINK ------------------------------------------------------------------------------
			blink = ' '.join(format(ord(x), 'b') for x in printable_text)
			pin0 = 17
			pin1 = 27
			GPIO.setup(pin0, GPIO.OUT)
			GPIO.setup(pin1, GPIO.OUT)
			for n in blink:
				if n == "1":
					GPIO.output(17, 1)
					time.sleep(.00625)
					GPIO.output(17, 0)
					time.sleep(.00625)
				elif n == "0":
					GPIO.output(27, 1)
					time.sleep(.00625)
					GPIO.output(27, 0)
					time.sleep(.00625)
				else:
					time.sleep(.0125)

	def on_error(self, status_code, data):
		print status_code
		# self.disconnect()

def string_split(string, width):
	for start in range(0, len(string), width):
		yield string[start:start+width]

stream = TwitterStream(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
printer = ThermalPrinter("/dev/ttyAMA0", 19200, timeout=5)

pygame.mixer.init()
clock = pygame.time.Clock()
LANGUAGES = {'ca':'ca-es','zh':'zh-cn','da':'da-dk','nl':'nl-nl','fi':'fi-fi','fr':'fr-fr','de':'de-de','it':'it-it','ja':'ja-jp','ko':'ko-kr','nb':'nb-no','pl':'pl-pl','pt':'pt-br','ru':'ru-ru','es':'es-mx','sv':'sv-se'}
GPIO.setmode(GPIO.BCM)

while True:
	current_trend = twitter.get_place_trends(id=23424977
)[0]['trends'][0]['name']
	start_mins = int(time.time() / 60)
	print "***** NOW TRENDING: " + current_trend + " *****"
	printer.upsideDownOn()
	printer.inverseOn()
	printer.println((" *NOW TRENDING: " + current_trend + "* ").ljust(32))
	printer.feed(1)
	printer.inverseOff()
	printer.upsideDownOff()
	stream.statuses.filter(track=current_trend)
	GPIO.cleanup()





