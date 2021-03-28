import os
import json
import math


def getTotalFileCount():
  f = open("fileCount.txt")
  count = f.readline()
  f.close()
  return int(count)

def mergeTermDicts(termDicts) -> dict:
  mergedTerms = termDicts[0]
  dictNum = 1
  currentDict = termDicts[0]
  while dictNum < len(termDicts):
    mergeDict = termDicts[dictNum]
    for file in mergeDict.keys():
      if file in mergedTerms.keys():
        mergeTFIDF = ((1 + math.log(mergeDict[file])) * math.log(float(getTotalFileCount() / len(mergeDict))))
        mergedTerms[file] += mergeTFIDF
      elif file in currentDict.keys():
        currentTFIDF = ((1 + math.log(currentDict[file])) * math.log(float(getTotalFileCount() / len(currentDict))))
        mergeTFIDF = ((1 + math.log(mergeDict[file])) * math.log(float(getTotalFileCount() / len(mergeDict))))
        mergedTerms[file] = currentTFIDF + mergeTFIDF
    dictNum += 1
  return mergedTerms
  

def displayResults(sortedFiles):
  filecount = 0
  while filecount < 15:
    if filecount < len(sortedFiles):
      with open(sortedFiles[filecount]) as f:
        jsonResult = json.load(f)
        f.close()
      print(jsonResult["url"])
    filecount += 1

def searchIndex(searchStr) -> list:
  searchTerms = searchStr.split(" ")
  print("Top Results in Index from Query " + str(searchTerms))
  termDicts = []

  for term in searchTerms:
    searchIndex = math.ceil(ord(term[0]) / 3) - 32 
    indexName = str("indexPart" + str(searchIndex) + ".json")
    try:
      with open(os.path.abspath(indexName)) as disk0:
        diskIndex = json.load(disk0)
      disk0.close()
      try:
        termDicts.append(diskIndex[term])
      except KeyError:
        pass
    except FileNotFoundError:
      print("Failed to open Index")
  
  if len(termDicts) == 0:
    return []
    
  mergedTermDicts = mergeTermDicts(termDicts)

  sorted_values = sorted(mergedTermDicts.values(), reverse=True) # Sort the values
  sorted_files = []
  for score in sorted_values:
    for file in mergedTermDicts.keys():
        if mergedTermDicts[file] == score:
          if file not in sorted_files:
            sorted_files.append(file)
            break

  displayResults(sorted_files)
    
