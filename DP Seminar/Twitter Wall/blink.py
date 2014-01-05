import binascii
from unidecode import unidecode
import time
import RPi.GPIO as GPIO

text = unidecode(u"Hello world! How are you?")
returned = ' '.join(format(ord(x), 'b') for x in text)

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(27, GPIO.OUT)

for n in returned:
	if n == "1":
		GPIO.output(17, 1)
		time.sleep(.0125)
		GPIO.output(17, 0)
		time.sleep(.0125)
	elif n == "0":
		GPIO.output(27, 1)
		time.sleep(.0125)
		GPIO.output(27, 0)
		time.sleep(.0125)
	else:
		time.sleep(.025)


