from flask import Blueprint, jsonify, abort, Response, request
from glob import glob
from gppp.folderLayout import FIRMWARES_FOLDER, GPPP_ROOT_FOLDER
from gppp.openocd import openocd_config_exists
import os
import threading
import subprocess
bp = Blueprint('firmware', __name__, url_prefix='/api/firmware')


class FlashThread(threading.Thread):
  def __init__(self, mcuName, firmwareFile):
    threading.Thread.__init__(self)
    self.mcuName = mcuName
    self.firmwareFile = firmwareFile
    self.exitCode = None
    self.running = False
    self.error = False
    self.finished = False
    self.stdout = ''
    self.stderr = ''

  def run(self):
    self.running = True

    cmds = [
        os.path.join(GPPP_ROOT_FOLDER, 'scripts', 'flash.py'),
        'flash',
        '--mcu-name',
        self.mcuName,
        '--firmware-file',
        self.firmwareFile
    ]

    p = subprocess.Popen(cmds, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    while True:
      code = p.poll()
      if code is not None:
        self.exitCode = code

        if code > 0:
          self.error = True

        break

    out, err = p.communicate()
    self.stderr = err.decode()
    self.stdout = out.decode()

    self.running = False
    self.finished = True


def firmwareFileExists(filename: str):
  if filename.startswith('..') or filename.startswith('.'):
    return False

  firmwarePath = os.path.join(FIRMWARES_FOLDER, filename)
  return os.path.exists(firmwarePath)


@bp.get('/')
def getFirmwares():
  firmwarePaths = glob(FIRMWARES_FOLDER + '/**/*', recursive=True)

  firmwareData = []

  for firmwarePath in firmwarePaths:
    firmwareStat = os.stat(firmwarePath)
    firmwareData.append({
        'filename': firmwarePath.replace(FIRMWARES_FOLDER + '/', ''),
        'filesize': firmwareStat.st_size,
        'created': firmwareStat.st_ctime
    })

  return jsonify(firmwareData)


@bp.post('/')
def saveFirmware():
  for fname in request.files:
    f = request.files.get(fname)
    f.save(os.path.join(FIRMWARES_FOLDER, fname))

  return getFirmware(fname)


@bp.get('/<filename>')
def getFirmware(filename: str):
  if not firmwareFileExists(filename):
    abort(404)

  firmwarePath = os.path.join(FIRMWARES_FOLDER, filename)
  firmwareStat = os.stat(firmwarePath)

  firmwareData = {
      'filename': filename,
      'filesize': firmwareStat.st_size,
      'created': firmwareStat.st_ctime
  }

  return jsonify(firmwareData)


@bp.delete('/<filename>')
def deleteFirmware(filename: str):
  if not firmwareFileExists(filename):
    abort(404)

  firmwarePath = os.path.join(FIRMWARES_FOLDER, filename)

  os.remove(firmwarePath)

  return Response(status=202)


flashThread: FlashThread = None


@bp.post('/flash')
def flashFirmware():

  global flashThread

  if flashThread is not None:
    if flashThread.running:
      abort(400, description='A flash task is already running')

  firmware = request.form.get('firmware')
  mcuName = request.form.get('mcuName')

  if not firmwareFileExists(firmware):
    abort(404, description='Firmware %s does not exist' % firmware)

  if not openocd_config_exists(mcuName):
    abort(404, description='MCU %s does not exist' % mcuName)

  firmwarePath = os.path.join(FIRMWARES_FOLDER, firmware)

  flashThread = FlashThread(mcuName, firmwarePath)
  flashThread.start()

  res = {
      'firmware': firmware,
      'mcuName': mcuName,
      'message': 'Flash task started'
  }

  return jsonify(res)


@bp.get('/flash')
def getFlashSttaus():

  global flashThread

  if flashThread is None:
    abort(404, 'No one started a flash task')

  res = {
      'stdout': flashThread.stdout,
      'stderr': flashThread.stderr,
      'running': flashThread.running,
      'error': flashThread.error,
      'finished': flashThread.finished,
      'editCode': flashThread.exitCode,
      'mcuName': flashThread.mcuName,
      'firmwareFile': flashThread.firmwareFile
  }

  return jsonify(res)
