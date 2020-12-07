import subprocess
import os
import argparse

sumoConfigEndWith = 'sumocfg'

def choicesSumoFile():
  sumoPath = os.path.dirname(os.path.abspath(__file__))
  return [f for f in os.listdir(sumoPath) if f.endswith(f'.{sumoConfigEndWith}')]

fileNameSumoConfig = choicesSumoFile()

parser = argparse.ArgumentParser(description='параменты для скрипта')
parser.add_argument('fileSumo', default=fileNameSumoConfig[0], choices=fileNameSumoConfig, help=f'что-то из этого {fileNameSumoConfig}')
args = parser.parse_args()
fileSumo = args.fileSumo

homeDir = os.environ.get("SUMO_HOME", os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
exePath = os.path.join(homeDir, "bin", 'sumo-gui')
if os.path.exists(exePath) or os.path.exists(exePath + ".exe"):
  subprocess.call([exePath, "-c", fileSumo])
else:
  print("Warning! %s not found." % exePath)
