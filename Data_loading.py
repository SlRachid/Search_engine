import os
import py7zr

MAIN_PATH = ".\Search_engine"
DATA_PATH = ".\Search_engine\data"

#os.mkdir(DATA_PATH)

archive = py7zr.SevenZipFile(DATA_PATH + '\cstheory.stackexchange.com.7z', mode='r')
archive.extractall(path=os.path.join(MAIN_PATH, 'data'))
archive.close()
