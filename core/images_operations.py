from os import listdir
from PIL import Image, ImageOps
import numpy as np

def checkIfIsAorB(file):
    return file.split("_")[1]


def calculateMediumImageOfFolder(folderPath):
    files = [f for f in listdir(folderPath)]

    readyImages = []

    for f in files:
        if checkIfIsAorB(f) == 'a':
            readyImages.append(np.asarray(Image.open(folderPath + f)))
        else:
            img = ImageOps.flip(Image.open(folderPath + f))
            img = ImageOps.mirror(img)
            readyImages.append(np.asarray(img))

    mediumImage = np.sum(readyImages, axis=0)/len(files)
    return mediumImage

def calculateTheMostNearImageToMeanImage(folder):

    meanImage = calculateMediumImageOfFolder(folder)

    files = [f for f in listdir(folder)]

    readyImages = []

    for f in files:
        if checkIfIsAorB(f) == 'a':
            readyImages.append(np.asarray(Image.open(folder + f)))
        else:
            img = ImageOps.flip(Image.open(folder + f))
            img = ImageOps.mirror(img)
            readyImages.append(np.asarray(img))

    errors = []

    for img in readyImages:
        e = np.sum(np.square(meanImage - img))
        errors.append(e)

    i = errors.index(np.min(errors))

    return readyImages[i], files[i]


def flipAllBTypeImagesFromFolder(folder, typeFlip):
    files = [f for f in listdir(folder)]
    for f in files:
        if checkIfIsAorB(f) == 'b':
            img = None
            if typeFlip=='x':
                img = ImageOps.flip(Image.open(folder + f))
            if typeFlip=='y':
                img = ImageOps.mirror(Image.open(folder + f))
            else:
                img = ImageOps.flip(Image.open(folder + f))
                img = ImageOps.mirror(img)

            img.save(folder + f)



