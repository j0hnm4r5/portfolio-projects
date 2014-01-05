# -*- coding: utf-8 -*-

from Queue import Queue
from threading import Thread
from twython import TwythonStreamer
from twitterCredentials import *

import time

class StreamThread(Thread):

	def __init__(self, stream_to_animate_queue):
		Thread.__init__(self)
		self.stream_to_animate_queue = stream_to_animate_queue

	def run(self):
		print "RUNNING"
		self.stream = LiveStream(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET, self.stream_to_animate_queue)
		print "STREAM INITIALIZED"
		# self.stream.statuses.filter(track="space")
		self.stream.statuses.sample()
		print "STREAM DONE"

class LiveStream(TwythonStreamer):

	def __init__(self, APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET, stream_to_animate_queue):
		super(LiveStream, self).__init__(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
		self.stream_to_animate_queue = stream_to_animate_queue
		self.i = 1

	def on_success(self, data):
		if 'user' in data:
			if 'screen_name' in data['user']:
				username = data['user']['screen_name'].encode('utf-8')
		else:
			username = "ANONYMOUS-USER"

		if 'text' in data:
			tweet = " ↩ ".join(data['text'].encode('utf-8').split("\n"))
			self.stream_to_animate_queue.put((username,tweet))
			print tweet

	def on_error(self, status_code, data):
		print('Error: {0}'.format(status_code))

class AnimateThread(Thread):
	"""CUURENTLY JUST PRINTING TO CONSOLE"""
	def __init__(self, stream_to_animate_queue):
		Thread.__init__(self)
		self.stream_to_animate_queue = stream_to_animate_queue

	def run(self):
		while True:
			item = self.stream_to_animate_queue.get()
			username = item[0]
			tweet = item[1]
			print "@" + username + ": " + tweet
			self.stream_to_animate_queue.task_done()



stream_to_animate_queue = Queue()

streaming = StreamThread(stream_to_animate_queue)
# animation = AnimateThread(stream_to_animate_queue)

streaming.start()
# animation.start()
