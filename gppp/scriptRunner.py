import subprocess
import sys
from os import path
from gppp.folderLayout import SCRIPTS_FOLDER


def runScript(scriptName, sudo=False):
  script = path.join(SCRIPTS_FOLDER, scriptName + '.sh')

  scriptArgs = [script,]
  if sudo:
    scriptArgs.insert(0, 'sudo')

  p = subprocess.Popen(scriptArgs, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  while True:
    out = p.stderr.read(1)
    if p.poll() is not None:
      break

    if out != '':
      sys.stdout.write(out.decode())
      sys.stdout.flush()

  sys.stdout.write('Return code: %s \n' % p.returncode)
  sys.stdout.flush()
