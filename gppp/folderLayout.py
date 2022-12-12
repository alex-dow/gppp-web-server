from os import path

GPPP_FOLDER = path.abspath(path.join(path.expanduser('~'), '.gppp'))
FIRMWARES_FOLDER = path.join(GPPP_FOLDER, 'firmwares')
LOGS_FOLDER = path.join(GPPP_FOLDER, 'logs')
SCRIPTS_FOLDER = path.join(path.dirname(__file__), 'scripts')
OPENOCD_FOLDER = path.join(path.expanduser('~'), 'openocd')
GPPP_ROOT_FOLDER = path.abspath(path.join(path.dirname(__file__), '..'))
