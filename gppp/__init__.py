from flask import Flask
from os import path, makedirs

GPPP_FOLDER = path.join(path.expanduser('~'), '.gppp')
FIRMWARES_FOLDER = path.join(GPPP_FOLDER, 'firmwares')
LOGS_FOLDER = path.join(GPPP_FOLDER, 'logs')


def create_app():
  app = Flask(__name__)

  @app.route('/test')
  def test():
    return '<h1>GPPP Test</h1>'

  for f in [ FIRMWARES_FOLDER, LOGS_FOLDER ]:
    if not path.exists(f):
      makedirs(f)

  from gppp import firmware
  app.register_blueprint(firmware.bp)

  return app