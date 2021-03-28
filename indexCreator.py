import os
import json
import re
import math
from bs4 import BeautifulSoup
######################


fileCount = 0
######################


def BuildIndex(path):
  filePaths     = GetAllFilePaths(path)
  indexBatchCap = 1000

  n = 0
  while len(filePaths) != 0:
    if indexBatchCap > len(filePaths):
      indexBatchCap = len(filePaths)
     
    batch = filePaths[0:indexBatchCap]
    del filePaths[0:indexBatchCap]

    partialIndex = ParseBatch(batch)

    name  = "partialIndex" + str(n) + ".json"
    with open(name, "w") as disk:
      json.dump(partialIndex, disk, indent = 4)
    disk.close()
    
    n += 1
  
  mergeJson()
  
  with open("fileCount.txt", 'w') as f:
    f.write('%d' % fileCount)
######################

  
def mergeJson():
  name = str(os.path.abspath("partialIndex0.json"))
  indexNum = 0
  while True:
    try:
      diskRead     = open(str(os.path.abspath(name)), 'r')
      diskReadJson = json.loads(diskRead.read())
      diskRead.close()
      os.remove(str(os.path.abspath(name)))
    except FileNotFoundError:
      break

    dictList = []
    while len(dictList) < 10:
      dictList.append(dict())

    for token in diskReadJson.keys():
      indexDestination = math.ceil(ord(token[0]) / 3) - 33
      if (0 <= indexDestination < len(dictList)):
        dictList[indexDestination][token] = diskReadJson[token]
      
    fileDestination = 1
    while fileDestination < len(dictList):
      indexName = str("indexPart" + str(fileDestination) + ".json")
      if (os.path.isfile(indexName)):
        with open(os.path.abspath(indexName)) as indexPart:
          indexPartDict = json.load(indexPart)
          indexPart.close()
          indexPartDict.update(dictList[fileDestination - 1])
      else:
        indexPartDict = {}
        indexPartDict = dictList[fileDestination - 1]
        
      with open(os.path.abspath(indexName), 'w') as indexPart:
        indexPartDict = json.dump(indexPartDict, indexPart, indent = 4)
        indexPart.close()
      fileDestination += 1
    
    indexNum += 1
    name = "partialIndex" + str(indexNum) + ".json"
#####################

    
def dictUnion(dict1, dict2) -> dict:
  for token in dict1:
    if token in dict2:
      dict1[token].update(dict2[token])
      #dict2.remove(token)

  dict2.update(dict1)
  
  return dict2
######################


def ParseBatch(batch) -> dict:
  partialIndex = dict()

  # ... parse tokens
  
  for file in batch:
    try:
      fileText = open(file, 'r')
      global fileCount
      fileCount += 1
      try:
        jsonContent = json.loads(fileText.read())

        soup    = BeautifulSoup(jsonContent["content"], 'html.parser')   
        soup    = soup.get_text()
        tokens  = soup.split()

        #CLEAN UP TOKENS
        for token in tokens:
          if "http" in token or ".com" in token:
            pass
          else:
            token = re.sub('[^a-zA-Z]+', "", token)
          if len(token) > 2:
            token = token.lower()
            if token not in partialIndex:
              partialIndex[token] = {file:1}
            elif file in partialIndex[token]:
              partialIndex[token][file] += 1
            else:
              partialIndex[token].update({file:1})

      except ValueError:
        pass
      fileText.close()
    except FileNotFoundError:
      print("FAILED TO OPEN FILE")

  return partialIndex
######################


def GetAllFilePaths(path) -> list:
  filepaths = []
  for root, dirs, files in os.walk(path):
    for file in files:
      filepaths.append(os.path.join(root,file))
  
  return filepaths
######################

