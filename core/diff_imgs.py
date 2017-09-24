import os
import cv2
from os import listdir

path = "/Users/MedicalWS/Documents/Thermographie/PostProcess/Bregy"
path_a = path + "/Diferencias8" + "/Dif_a/"
path_b = path + "/Diferencias8" + "/Dif_b/"

files_a = [f for f in listdir(path_a)]
files_b = [f for f in listdir(path_b)]

for i in range(0, len(files_a)):




