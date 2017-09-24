from tkinter import filedialog as fd
from os import listdir
import cv2
import numpy as np
from registro1 import RigidRegistration
from registro2 import BSplineRegistration
import os
from detechToTags import detech2tags
import matplotlib.pyplot as plt

# get File put in Ordenado folder
#path_in = fd.askdirectory()
#onlyfiles = [f for f in listdir(path_in)]

#path_out = fd.askdirectory()
#detech2tags(path_in, path_out)

# get Files, flip and put in folders D8, D10, D12
numero = "8"
dist = "_" + numero + "_"
file1 = "D" + numero + "/"
file2 = "D" + numero + "_Rigido/"
file3 = "D" + numero + "_BSpline/"
path_out = "/Users/MedicalWS/Documents/Thermographie/PostProcess/Paciente25/Ordenado"

onlyfiles = [f for f in listdir(path_out)]
matching_dist = [s for s in onlyfiles if dist in s]
# for a
matching = [s for s in matching_dist if "a" in s]
alist = sorted([[f.split('0d')[1], f] for f in matching], key=lambda r:r[0])
list8 = []
cont = 0
for f in matching:
    list8.append(alist[cont][1])
    cont += 1
# for b
matching = [s for s in matching_dist if "b" in s]
alist = sorted([[f.split('0d')[1], f] for f in matching], key=lambda r:r[0])
cont = 0
for f in matching:
    list8.append(alist[cont][1])
    cont += 1

for i in range(0,len(list8)):
    image = cv2.imread(path_out + "/" + list8[i])
    directory = path_out.split('Ordenado')[0] + file1
    if not os.path.exists(directory):
        os.makedirs(directory)
    if i < len(list8)/2:
        cv2.imwrite(directory + list8[i], image)
    else:
        cv2.imwrite(directory + list8[i], cv2.flip(image,1))

# Imagen de Referencia, media
rows, cols = image.shape[:2]
tot_img = np.empty(shape=(rows*cols,len(list8)), dtype='float64')
for i in range(0,len(list8)):
    image = cv2.imread(directory + list8[i])
    img_col = np.array(image[:,:,1], dtype='float64').flatten()
    tot_img[:, i] = img_col[:]

mean_img_col = np.sum(tot_img, axis=1)/len(list8)
norm_tot = np.empty(shape=(1,len(list8)), dtype='float64')

for i in range(0,len(list8)):
    tot_img[:, i] -= mean_img_col
    norm_tot[:, i] = np.linalg.norm(tot_img[:, i], axis=0)

reference = np.argmin(norm_tot)
print(reference)

# Rigid Registration
directory = path_out.split('Ordenado')[0] + file2
if not os.path.exists(directory):
    os.makedirs(directory)
fixedI = path_out.split('Ordenado')[0] + file1 + list8[reference]
cv2.imwrite(directory + list8[reference], cv2.imread(fixedI))
for i in range(0, len(list8)):
    if i != reference:
        movedI = path_out.split('Ordenado')[0] + file1 + list8[i]
        image_reg = RigidRegistration(fixedI, movedI)
        cv2.imwrite(directory + list8[i], image_reg)
'''
# BSpline Registration
directory = path_out.split('Ordenado')[0] + file3
if not os.path.exists(directory):
    os.makedirs(directory)
fixedI = path_out.split('Ordenado')[0] + file2 + list8[reference]
cv2.imwrite(directory + list8[reference], cv2.imread(fixedI))
for i in range(0, len(list8)):
    if i != reference:
        movedI = path_out.split('Ordenado')[0] + file2 + list8[i]
        image_reg = BSplineRegistration(fixedI, movedI)
        cv2.imwrite(directory + list8[i], image_reg)
'''
