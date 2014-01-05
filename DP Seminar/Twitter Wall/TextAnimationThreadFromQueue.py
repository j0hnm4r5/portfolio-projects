import sys

import pygame
from pygame.locals import *

from Queue import Queue
from threading import Thread, Event

class AnimateThread(Thread):

	black = (0,0,0)
	white = (255,255,255)

	fps_limit = 60

	def __init__(self, stream_to_animate_queue, animate_to_printer_queue):

		Thread.__init__(self)

		self._stop = Event()

		self.stream_to_animate_queue = stream_to_animate_queue
		self.animate_to_printer_queue = animate_to_printer_queue

		pygame.init()

		# self.screen = pygame.display.set_mode((0,0), FULLSCREEN)
		self.screen = pygame.display.set_mode((800,800))
		self.screen_height = self.screen.get_height()
		self.screen_width = self.screen.get_width()


		self.clock = pygame.time.Clock()

		self.font = pygame.font.Font('/Users/johnmars/Library/Fonts/NeutraText-Book.otf', 16)

		self.live_text = [self.TextObject("STREAM INITIALIZED", self.screen, (0, 30), AnimateThread.black, self.screen_height, self.font)]



	def run(self):
		while self._stop.is_set() == False:
			# self.clock.tick(AnimateThread.fps_limit)
			self.screen.fill(AnimateThread.black)

			if self.stream_to_animate_queue.qsize() > 0:
				item = self.stream_to_animate_queue.get()
				text = self.TextObject(item, self.screen, (30, 0), AnimateThread.white, self.screen_height, self.font)
				self.live_text.append(text)
				self.stream_to_animate_queue.task_done()


			for i, item in enumerate(self.live_text):
				if item.y >= self.screen_height:
					self.live_text.remove(item)
					break
				if self.live_text[i-1].y >= 30:
					item.fall(2)

			pygame.display.update()
			self.interactions()
		pygame.quit()
		sys.exit()

	def stop(self):
		self._stop.set()

	class TextObject(object):
		def __init__(self, text_string, surface, (x,y), color, screen_height, font):
			self.font = font
			self.text_string = text_string
			self.surface = surface
			self.x = x
			self.y = y
			self.color = color
			self.screen_height = screen_height
			self.text = self.font.render(self.text_string, True, self.color)

		def fall(self, speed):
			if self.y <= self.screen_height:
				self.surface.blit(self.text, (self.x, self.y))
				self.y += speed


	def interactions(self):
		for event in pygame.event.get():
			if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or event.type == QUIT:
				self.stop()


stream_to_animate_queue = Queue()
animate_to_printer_queue = Queue()

for i in range(20):
	stream_to_animate_queue.put("This is number " + str(i + 1))

animation = AnimateThread(stream_to_animate_queue, animate_to_printer_queue)
animation.start()

