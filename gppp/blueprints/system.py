from flask import Blueprint
from gppp.scriptRunner import runScript
bp = Blueprint('system', __name__, url_prefix='/api/system')


@bp.post('/reboot')
def getFirmwares():

  runScript('reboot', sudo=True)
  return 'reboot'
