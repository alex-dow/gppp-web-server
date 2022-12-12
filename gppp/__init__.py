from flask import Flask
from os import path, makedirs
from gppp.config import init_config as init_gppp_config, config
from gppp.signalLights import on_server_status
from gppp.openocd import save_openocd_config
import RPi.GPIO as GPIO
from gppp.folderLayout import FIRMWARES_FOLDER, LOGS_FOLDER


def init_pins():
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(config['gpio_status_led'], GPIO.OUT)


def init_config():
  init_gppp_config()

  save_openocd_config('yaw', config['gpio_yaw_mcu_swclk'], config['gpio_yaw_mcu_swdio'])
  save_openocd_config('roll', config['gpio_roll_mcu_swclk'], config['gpio_roll_mcu_swdio'])
  save_openocd_config('pitch', config['gpio_pitch_mcu_swclk'], config['gpio_pitch_mcu_swdio'])


def create_gppp_app():
  app = Flask(__name__)

  for f in [FIRMWARES_FOLDER, LOGS_FOLDER]:
    if not path.exists(f):
      makedirs(f)

  from gppp.blueprints import firmware
  from gppp.blueprints import system
  app.register_blueprint(firmware.bp)
  app.register_blueprint(system.bp)

  init_config()
  init_pins()
  on_server_status()

  return app
