#pip3 install xmltodict

import csv
import xmltodict

def readInputFile(nameFile):
  csv_reader = csv.reader(nameFile, delimiter=';')
  header = next(csv_reader)

  od = []

  if header != None:
    for column in header[1:]:
      for rows in csv_reader:
        row = rows[0]
        for car in rows[1:]:
          if int(car) != 0:
            od.append({
              '@amount': int(car),
              '@origin': column,
              '@destination': row
            })

  file_name = f'{nameFile.name}.trips.xml'
  with open(file_name, 'w') as x_file:
    x_file.write(xmltodict.unparse({
      'actorConfig': {
        '@id': 0,
        'timeSlice': {
          '@duration': 3600000,
          '@startTime': 0,
          'odPair': od
        }
      }
    }, pretty=True))

if __name__ == "__main__":
  with open("morning40.csv") as file:
    readInputFile(file)