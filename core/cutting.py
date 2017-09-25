from os import listdir
from PIL import Image, ImageOps
import argparse


def cropImages(inputFolder, outputFolder, pads):
    files = [f for f in listdir(inputFolder)]

    for f in files:
        img = Image.open(inputFolder + f)
        img = img.crop(pads)
        img.save(outputFolder + f)


parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', help='Input folder', required=True)
parser.add_argument('-o', '--output', help='output folder', required=True)

parser.add_argument('-p', '--pads', help='Pads for bounding', required=True, type=str)

args = parser.parse_args()

inputFolder = args.input
outputFolder = args.output
#pads = (args.x, args.y, args.w, args.h)

pads = [int(s) for s in args.pads.split(',')]

print pads

cropImages(inputFolder, outputFolder, pads)
