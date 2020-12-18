#pip3 install xmltodict

import csv
from io import TextIOWrapper
import xmltodict
from os.path import join
import subprocess
import os
import argparse

configPath = os.path.dirname(os.path.abspath(__file__))
odPath = join(configPath, 'out_in', 'od')

def readInputFile(odf):
  file_path, type = odf
  with open(file_path) as file:
    csv_reader = csv.reader(file, delimiter=';')
    header = next(csv_reader)

    od = []

    if header != None:
      for rows in csv_reader:
        row = rows[0]
        for idx, car in enumerate(rows[1:]):
          if int(car) != 0:
            od.append({
              '@amount': int(car),
              '@origin': header[idx + 1],
              '@destination': row
            })

  return {
      '@id': type,
      'timeSlice': {
          '@duration': 3600000,
          '@startTime': 0,
          'odPair': od
      }
  }

def aggOD(actorConfig: list, folder: str):
    file_name = join(odPath, f'{folder}.od.xml')
    with open(file_name, 'w') as x_file:
      x_file.write(xmltodict.unparse({
          'demand': {
              '@xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance',
              '@xsi:noNamespaceSchemaLocation': 'http://sumo.dlr.de/xsd/amitran/od.xsd',
              'actorConfig': actorConfig
        }
      }, pretty=True))

    return file_name

def get_path_file(folder: str):
  return [(join(odPath, folder, f), f.split('_')[0]) for f in os.listdir(join(odPath, folder)) if f.endswith(f'.csv')]

def od_trips(file_name: str, folder: str):
  homeDir = os.environ.get("SUMO_HOME")
  exePath = join(homeDir, "bin", 'od2trips')
  if os.path.exists(exePath) or os.path.exists(exePath + ".exe"):
    subprocess.call([exePath, "-c", join(odPath, 'config.od2trips'),
                     '--od-amitran-files', file_name, '--output-file', join(odPath, f'{folder}.trips.xml')])
  else:
    print("Warning! %s not found." % exePath)

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='параменты для скрипта')
  parser.add_argument('folder')
  args = parser.parse_args()
  folder = args.folder

  od_trips(aggOD([readInputFile(f) for f in get_path_file(folder)], folder), folder)
