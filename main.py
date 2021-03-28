import os
from indexCreator import BuildIndex
from indexSearch import searchIndex



if __name__ == '__main__':
  filepath = os.getcwd()

  #CHANGE THIS TO '/folder_containing_files_to_index
  filepath += "/DEV"

  while True:
    userOption = input("Enter 'SEARCH' to search pre-existing index, \n or enter 'BUILD' to index files and search: ")
    if userOption.lower() == "build":
      BuildIndex(filepath)
      searchStr = input("Enter Search Query: ")
      searchIndex(searchStr)
      break
    elif userOption.lower() == "search":
      searchStr = input("Enter Search Query: ")
      searchIndex(searchStr)
      break
    else:
      print("Invalid input")
    
