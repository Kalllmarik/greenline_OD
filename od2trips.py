import subprocess
import os
import argparse

configEndWith = 'od2trips'

def choicesConfig():
  configPath = os.path.dirname(os.path.abspath(__file__))
  return [f for f in os.listdir(configPath) if f.endswith(f'.{configEndWith}')]


fileNameConfig = choicesConfig()

parser = argparse.ArgumentParser(description='параменты для скрипта')
parser.add_argument(
    'file', default=fileNameConfig[0], choices=fileNameConfig, help=f'что-то из этого {fileNameConfig}')
args = parser.parse_args()
file = args.file

homeDir = os.environ.get("SUMO_HOME", os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
exePath = os.path.join(homeDir, "bin", configEndWith)
if os.path.exists(exePath) or os.path.exists(exePath + ".exe"):
  subprocess.call([exePath, "-c", file])
else:
  print("Warning! %s not found." % exePath)
