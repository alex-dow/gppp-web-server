#!/usr/bin/env python3
import sys
import os
import argparse
import subprocess
import time
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from gppp.folderLayout import OPENOCD_FOLDER, GPPP_FOLDER  # noqa

parser = argparse.ArgumentParser(
    prog='GPPP Firmware Flash Script',
    description='Handles the task of flashing a firmware file to a connected MCU',
    epilog='Currently designed to flash RP2040 only'
)

parser.add_argument('command', choices=['flash', 'ping'])
parser.add_argument('--mcu-name', help='MCU Name to flash. Values can be "pitch", "yaw", or "roll"')
parser.add_argument('--firmware-file')
parser.add_argument('--timeout', default=300)


def run_openocd(mcuName, cmds, timeout):

  configFile = os.path.join(GPPP_FOLDER, 'openocd_' + mcuName + '.cfg')

  os.chdir(os.path.join(OPENOCD_FOLDER, 'bin'))
  cmds = [
      './openocd',
      '-f',
      configFile,
      '-f',
      'target/rp2040.cfg',
      '-c',
      cmds

  ]

  os.chdir(os.path.join(OPENOCD_FOLDER, 'bin'))
  startTime = time.time()
  p = subprocess.Popen(cmds, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

  while True:
    curtime = time.time()
    if (curtime - startTime) > timeout:
      print("OpenOCD timed out")
      p.kill()
      break
    exitCode = p.poll()
    if exitCode is not None:
      if exitCode > 0:
        print("OpenOCD failed with code %s" % exitCode)
      else:
        print("OpenOCD executed successfully")

      break

  stdout, stderr = p.communicate()

  print("--- openocd stdout ---")
  print(stdout.decode())
  print("--- openocd stderr ---")
  print(stderr.decode())


def flashFirmware(mcuName, firmwareFile, timeout):
  cmds = 'program %s verify reset exit' % firmwareFile
  run_openocd(mcuName, cmds, timeout)


def ping(mcuName, timeout):
  cmds = 'init; dap info; shutdown'
  run_openocd(mcuName, cmds, timeout)


def main():
  args = parser.parse_args()
  print(args)

  if (args.command == 'ping'):
    ping(args.mcu_name, args.timeout)
  elif (args.command == 'flash'):
    flashFirmware(args.mcu_name, args.firmware_file, args.timeout)
  else:
    raise RuntimeError("Invalid command")


if __name__ == "__main__":
  main()
