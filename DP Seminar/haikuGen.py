import string
from wordnik import *
import unirest
import HTMLParser
from unidecode import unidecode
from twython import TwythonStreamer
from twitterCredentials import *

class MyStreamer(TwythonStreamer):
	def on_success(self, data):
		try:
			if 'text' in data:
				if data['lang'] == "en":
					# print " "
					# print data['text']
					sentence = unidecode(HTMLParser.HTMLParser().unescape(data['text']))
					split = sentence.split()

					for i, word in enumerate(split):
						if "#" in word:
							del split[i]
						elif "@" in word:
							del split[i]
						elif "http" in word:
							del split[i]
						elif word == "RT":
							del split[i]
						else:
							split[i] = word.translate(string.maketrans("",""), string.punctuation).lower()

					# print string.join(split, " ")

					sylls = 0
					for i, word in enumerate(split):
						if sylls <= 17:

							spellcheck = unirest.get("https://montanaflynn-spellcheck.p.mashape.com/check/?text=" + word, headers={"X-Mashape-Authorization": "LnLwKk8panExUqzX8v7cuuJs3yqy11RL"})

							word = spellcheck.body['suggestion'].encode('utf-8')
							split[i] = word

							if word == "dint":
								word = "didn't"

							syllables = wordnik.getHyphenation(word)

							if syllables != None:
								if syllables == 0:
									sylls += 100
								else:
									# print len(syllables),
									sylls += len(syllables)
							else:
								# if the word is unrecognizable, just make the haiku fail.
								sylls += 100
								# print " "

					if 0 < sylls <= 17:
						# print " "
						# print sylls
						text = string.upper(string.join(split, " "))
						print sylls, text

						# numbers = {1:"one", 2:"two", 3:"three", 4:"four", 5:"five", 6:"six", 7:"seven", 8:"eight", 9:"nine", 10:"ten", 11:"eleven", 12:"twelve", 13:"thirteen", 14:"fourteen", 15:"fifteen", 16:"sixteen", 17:"seventeen"}

						# file_number = numbers[sylls]
						# print 'syllableCount/' + str(sylls) + '.txt'
						with open('syllableCount/' + str(sylls) + '.txt', 'a') as f:
							f.write(text + "\n")
							

		except:
			pass
		

stream = MyStreamer(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

apiUrl = 'http://api.wordnik.com/v4'
apiKey = 'f48e98c7cbdd0dd42f00f0e12640eb690a77dbc9a1581e338'
client = swagger.ApiClient(apiKey, apiUrl)
wordnik = WordApi.WordApi(client)



stream.statuses.sample()
