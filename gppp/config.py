import os
from gppp.folderLayout import GPPP_FOLDER
from typing import TypedDict, cast
import json

CONF_FILE = os.path.join(GPPP_FOLDER, 'config.ini')


class GpppConfig(TypedDict):
  gpio_status_led: int
  gpio_yaw_mcu_swclk: int
  gpio_yaw_mcu_swdio: int
  gpio_roll_mcu_swclk: int
  gpio_roll_mcu_swdio: int
  gpio_pitch_mcu_swclk: int
  gpio_pitch_mcu_swdio: int


config = GpppConfig(
    gpio_pitch_mcu_swclk=27,
    gpio_pitch_mcu_swdio=22,
    gpio_roll_mcu_swclk=6,
    gpio_roll_mcu_swdio=5,
    gpio_yaw_mcu_swclk=19,
    gpio_yaw_mcu_swdio=13,
    gpio_status_led=26
)


def save_config():
  global config
  j = json.dumps(config, indent=4)
  with open(CONF_FILE, 'w') as cf:
    cf.write(j)


def init_config():
  global config
  if not os.path.exists(CONF_FILE):
    save_config()
  else:
    with open(CONF_FILE, 'r') as cf:
      j = cf.read()
      config = cast(GpppConfig, j)
