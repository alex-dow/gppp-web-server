import RPi.GPIO as GPIO
from gppp.config import config


def on_server_status():
  pin = config['gpio_status_led']
  GPIO.output(pin, GPIO.HIGH)


def off_server_status():
  pin = config['gpio_status_led']
  GPIO.output(pin, GPIO.LOW)
