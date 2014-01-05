from twython import TwythonStreamer
from twitterCredentials import *
import pprint
import requests
import pygame
import time, sys, os


class MyStreamer(TwythonStreamer):
	def on_success(self, data):
		global LANGUAGES
		if 'text' in data:

			params = {'key' : "6cfd2e1aca4a425dbdd9b427d52a3b21", 'hl' : "en-us", 'r' : "2", 'c' : "WAV"}

			print data['text']
			params['src'] = data['text']

			if 'lang' in data:
				if data['lang'] in LANGUAGES:
					params['hl'] = LANGUAGES.get(data['lang'])
					# print params['hl']

			r = requests.get('http://api.voicerss.org/', params=params)
			with open('tts.wav', 'wb') as f:
				f.write(r.content)
			pygame.mixer.music.load('tts.wav')
			pygame.mixer.music.play()
			while pygame.mixer.music.get_busy():
				clock.tick(5)
			# os.system('aplay -q tts.wav')
			os.remove('tts.wav')
		

stream = MyStreamer(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
pygame.mixer.init()
clock = pygame.time.Clock()
LANGUAGES = {'ca':'ca-es','zh':'zh-cn','da':'da-dk','nl':'nl-nl','fi':'fi-fi','fr':'fr-fr','de':'de-de','it':'it-it','ja':'ja-jp','ko':'ko-kr','nb':'nb-no','pl':'pl-pl','pt':'pt-br','ru':'ru-ru','es':'es-mx','sv':'sv-se'}

# stream.statuses.filter(track='risd')
stream.statuses.sample()

