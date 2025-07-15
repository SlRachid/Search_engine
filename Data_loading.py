import os
import py7zr

MAIN_PATH = "."
DATA_PATH = "data"

#os.mkdir(DATA_PATH)
print(os.getcwd())
archive = py7zr.SevenZipFile(os.path.join(DATA_PATH , 'cstheory.stackexchange.com.7z'), mode='r')
archive.extractall(path=os.path.join(MAIN_PATH, 'data'))
archive.close()
