from flask import Blueprint, jsonify, abort, Response, request
from glob import glob
from gppp import GPPP_FOLDER, FIRMWARES_FOLDER
import os
bp = Blueprint('firmware', __name__, url_prefix='/api/firmware')

def firmwareFileExists(filename: str):
  if filename.startswith('..') or filename.startswith('.'):
    return False

  firmwarePath = os.path.join(FIRMWARES_FOLDER, filename)
  return os.path.exists(firmwarePath)

@bp.get('/')
def getFirmwares():
  firmwarePaths = glob(FIRMWARES_FOLDER + '/**/*.hex', recursive=True)

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
