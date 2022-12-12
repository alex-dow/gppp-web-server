import os
from gppp.folderLayout import GPPP_FOLDER

openocd_cfg_template = """
# Use RPI GPIO pins
adapter driver bcm2835gpio

bcm2835gpio_speed_coeffs 146203 36

# GPIO Pins for SWD
bcm2835gpio_swd_nums  {swclk} {swdio}

# misc config
transport select swd
adapter speed 1000
"""


def get_cfg_path(name: str):
  return os.path.join(GPPP_FOLDER, 'openocd_' + name + '.cfg')


def save_openocd_config(name: str, swclk: int, swdio: int):
  cfg = openocd_cfg_template.format(swclk=swclk, swdio=swdio)
  cfgPath = get_cfg_path(name)

  with open(cfgPath, 'w') as cf:
    cf.write(cfg)


def openocd_config_exists(name):
  cfgPath = get_cfg_path(name)
  return os.path.exists(cfgPath)
