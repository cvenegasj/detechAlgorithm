from tkinter import filedialog as fd
from os import listdir
from detechToTags import detech2tags

# get File
path_in = fd.askdirectory()
onlyfiles = [f for f in listdir(path_in)]

path_out = fd.askdirectory()
detech2tags(path_in, path_out)


