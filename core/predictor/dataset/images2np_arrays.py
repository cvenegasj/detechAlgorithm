#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import division
import os
from detechToTags import detech2tags
from distutils.dir_util import copy_tree
from shutil import copyfile
import shutil
import uuid
import numpy as np
from PIL import Image

FIRST_PATH = 'first'
MIDDLE_PATH = 'temp'
#IMAGES_PATH = 'images'


class DetechImage:
    def __init__(self, name):
        peeks = name.split('_')
        self.name = peeks[0]
        self.metadata = '_'.join(peeks[1:-1])
        self.score = peeks[-1].replace('.jpg', '')

    def getNumericScore(self):
        try:
            return float(self.score.replace('d', '.'))
        except:
            return 0.0

    def getName(self):
        return '_'.join([self.name, self.metadata, self.score]) + '.jpg'

def normalDirToDetechWorkspace(inputDir, outputPath):
    detech2tags(inputDir, outputPath)


def folderImagesToUniqueFolder(inputDir, outputDir):
    patient = 0
    img = 0

    if not os.path.exists(FIRST_PATH):
        os.makedirs(FIRST_PATH)
    if not os.path.exists(MIDDLE_PATH):
        os.makedirs(MIDDLE_PATH)
    if not os.path.exists(outputDir):
        os.makedirs(outputDir)

    for root, dirs, files in os.walk(inputDir, topdown=False):
        for name in files:
            img += 1
        for name in dirs:
            rDir = 'patient' + str(patient)
            #os.renames(os.path.join(inputDir,name), rDir)
            copy_tree(os.path.join(inputDir,name), os.path.join(FIRST_PATH, rDir))
            temporalDir = os.path.join(MIDDLE_PATH, rDir)
            if not os.path.exists(temporalDir):
                os.makedirs(temporalDir)
            normalDirToDetechWorkspace(os.path.join(FIRST_PATH,rDir), temporalDir)
            patient += 1

    print('We have %d images and %d patients'%(img, patient))

    patient = 0
    img = 0

    for root, dirs, files in os.walk(MIDDLE_PATH, topdown=False):
            for nameDir in dirs:
                for root, dirs, files in os.walk(os.path.join(MIDDLE_PATH, nameDir), topdown=False):
                    for name in files:
                        fromPath = os.path.join(nameDir, name)

                        dimg = DetechImage(name)
                        dimg.name = '_'.join(['img'+str(img), 'pt'+str(patient)])
                        finalName = dimg.getName()
            
                        copyfile(os.path.join(MIDDLE_PATH, fromPath), os.path.join(outputDir, finalName))
                        img += 1
                patient += 1

    shutil.rmtree(FIRST_PATH)
    shutil.rmtree(MIDDLE_PATH)

def imagesDataToArrays(folderInput, output):

    files = [f for f in os.listdir(folderInput)]

    if not os.path.exists(output):
        os.makedirs(output)

    for f in files:
        img = DetechImage(f)
        f_array = np.asarray(Image.open(os.path.join(folderInput, f)))
        score = img.getNumericScore()
        uName = str(uuid.uuid4())

        f_array = np.asarray([f_array, score])
        np.save(os.path.join(output, uName), f_array)


imagesDataToArrays('/home/bregy/Desktop/detechAlgorithm/core/predictor/model/images', 'testOut')

