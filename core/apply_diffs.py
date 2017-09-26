from diffs_and_threshold import folderDiffsExtract
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('-i', '--input', help='Input folder', required=True)
parser.add_argument('-o', '--output', help='output folder', required=True)
parser.add_argument('-p', '--params', help='Parameter for difference mode', required=True, type=str)

args = parser.parse_args()

inputFolder = args.input
outputFolder = args.output
#pads = (args.x, args.y, args.w, args.h)

params = [s for s in args.params.split(',')]
print params

dist = str(params[0])
tsub = str(params[1])

if dist == '8' or dist=='10' or dist=='12' or dist=='all':
    if tsub == 't' or tsub == 'ab' or tsub == 'ba':
        print 'Applying differences at %s distance and type of subtract: %s'%(dist, tsub)
        folderDiffsExtract(inputFolder, outputFolder, dist, tsub)
    else:
        print 'Incorrect params'

else:
    print 'Incorrect params'

