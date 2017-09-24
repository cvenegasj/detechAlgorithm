from images_operations import calculateTheMostNearImageToMeanImage
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', help='Input folder', required=True)

args = parser.parse_args()
inputFolder = args.input
_, image = calculateTheMostNearImageToMeanImage(inputFolder)
print image