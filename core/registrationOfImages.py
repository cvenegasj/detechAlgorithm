import argparse
from os import listdir
import registro1 as reg
import images_operations as ops
from PIL import Image
import cv2

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', help='Input folder', required=True)
parser.add_argument('-o', '--output', help='output folder', required=True)

args = parser.parse_args()

print args

inputFolder = args.input
outputFolder = args.output

files = [f for f in listdir(inputFolder)]

mediumImage, nameOfMediumImage = ops.calculateTheMostNearImageToMeanImage(inputFolder)
ops.flipAllBTypeImagesFromFolder(inputFolder, 'y')
for f in files:
    # img = np.asarray(Image.open(inputFolder+f))
    # protoImg = reg.RigidRegistration(mediumImage, img, 'correlation', 'grad-desc')
    protoImg = reg.RigidRegistration(inputFolder+nameOfMediumImage, inputFolder+f, 'correlation', 'grad-desc')
    registeredImage = Image.fromarray(protoImg, 'L')

    if outputFolder[-1] == '/':
        # registeredImage.save(outputFolder+f)
        cv2.imwrite(outputFolder+f, protoImg)
    else:
        # registeredImage.save(outputFolder+'/'+f)
        cv2.imwrite(outputFolder+'/'+f, protoImg)