from os import listdir
from PIL import Image, ImageOps, ImageChops
import numpy as np


def sortByDetechTag(array):
    return sorted(array, key=lambda a: int(a.split('_')[0].replace("img", '')))


def folderDiffsExtract(inputFolder, outputFolder, dist='all', tsub='ab'):
    files = [f for f in listdir(inputFolder) if 'img' in f]

    if tsub=='ab' or tsub=='ba':
        a_files = []
        b_files = []
        for f in files:
            if '_a_' in f:
                a_files.append(f)
            else:
                b_files.append(f)

        a_files = sortByDetechTag(a_files)
        b_files = sortByDetechTag(b_files)

        if not len(a_files) == len(b_files):
            return

        if dist=='8' or dist==8:
            j = 1
            for i in range(len(a_files)):
                if a_files[i].split('_')[2] == '8':
                    im1Weight = float(a_files[i].split('_')[-1].replace('.jpg', '').replace('d','.'))
                    im2Weight = float(b_files[i].split('_')[-1].replace('.jpg', '').replace('d','.'))

                    img1 = Image.open(inputFolder + a_files[i])
                    img2 = Image.open(inputFolder + b_files[i])

                    if tsub[0] == 'ab':
                        diff = ImageChops.difference(img1, img2)
                        finalWeight = im1Weight - im2Weight
                    else: # or if tsub == 'ba'
                        diff = ImageChops.difference(img2, img1)
                        finalWeight = im2Weight - im1Weight

                    name = 'img' + str(j) + '_d8_' + str(finalWeight).replace('.', 'd') + '.jpg'
                    diff.save(outputFolder + name)
                    j += 1
                else:
                    pass

        elif dist=='10' or dist==10:
            j = 1
            for i in range(len(a_files)):
                if a_files[i].split('_')[2] == '10':
                    im1Weight = float(a_files[i].split('_')[-1].replace('.jpg', '').replace('d', '.'))
                    im2Weight = float(b_files[i].split('_')[-1].replace('.jpg', '').replace('d', '.'))

                    img1 = Image.open(inputFolder + a_files[i])
                    img2 = Image.open(inputFolder + b_files[i])

                    if tsub[0] == 'ab':
                        diff = ImageChops.difference(img1, img2)
                        finalWeight = im1Weight - im2Weight
                    else:  # or if tsub == 'ba'
                        diff = ImageChops.difference(img2, img1)
                        finalWeight = im2Weight - im1Weight

                    name = 'img' + str(j) + '_d10_' + str(finalWeight).replace('.', 'd') + '.jpg'
                    diff.save(outputFolder + name)
                    j += 1
                else:
                    pass

        elif dist=='12' or dist==12:
            j = 1
            for i in range(len(a_files)):
                if a_files[i].split('_')[2] == '12':
                    im1Weight = float(a_files[i].split('_')[-1].replace('.jpg', '').replace('d', '.'))
                    im2Weight = float(b_files[i].split('_')[-1].replace('.jpg', '').replace('d', '.'))

                    img1 = Image.open(inputFolder + a_files[i])
                    img2 = Image.open(inputFolder + b_files[i])

                    if tsub[0] == 'ab':
                        diff = ImageChops.difference(img1, img2)
                        finalWeight = im1Weight - im2Weight
                    else:  # or if tsub == 'ba'
                        diff = ImageChops.difference(img2, img1)
                        finalWeight = im2Weight - im1Weight

                    name = 'img' + str(j) + '_d12_' + str(finalWeight).replace('.', 'd') + '.jpg'
                    diff.save(outputFolder + name)
                    j += 1
                else:
                    pass
        else:
            for i in range(len(a_files)):
                im1Weight = float(a_files[i].split('_')[-1].replace('.jpg', '').replace('d', '.'))
                im2Weight = float(b_files[i].split('_')[-1].replace('.jpg', '').replace('d', '.'))

                img1 = Image.open(inputFolder + a_files[i])
                img2 = Image.open(inputFolder + b_files[i])

                if tsub[0] == 'ab':
                    diff = ImageChops.difference(img1, img2)
                    finalWeight = im1Weight - im2Weight
                else:  # or if tsub == 'ba'
                    diff = ImageChops.difference(img2, img1)
                    finalWeight = im2Weight - im1Weight

                currentDist = '_' + a_files[i].split('_')[2] + '_'

                name = 'img' + str(i+1) + currentDist + str(finalWeight).replace('.', 'd') + '.jpg'
                diff.save(outputFolder + name)

    elif tsub=='t':
        a_files = []
        b_files = []
        for f in files:
            if '_a_' in f:
                a_files.append(f)
            else:
                b_files.append(f)

        a_files = sortByDetechTag(a_files)
        b_files = sortByDetechTag(b_files)

        if not len(a_files) == len(b_files):
            return

        x = 0
        y = 0
        z = 0

        absoluteCount = 1

        for i in range(0, len(a_files)):
            if a_files[i].split('_')[2] == '8':
                # print "--(8a)--> %s %d, %d"%(a_files[i], i, x)
                if not i == 0:
                    im1AWeight = float(a_files[x].split('_')[-1].replace('.jpg', '').replace('d', '.'))
                    im2AWeight = float(a_files[i].split('_')[-1].replace('.jpg', '').replace('d', '.'))
                    imgA1 = Image.open(inputFolder + a_files[x])
                    imgA2 = Image.open(inputFolder + a_files[i])

                    im1BWeight = float(b_files[x].split('_')[-1].replace('.jpg', '').replace('d', '.'))
                    im2BWeight = float(b_files[i].split('_')[-1].replace('.jpg', '').replace('d', '.'))
                    imgB1 = Image.open(inputFolder + b_files[x])
                    imgB2 = Image.open(inputFolder + b_files[i])

                    print "A: %s - %s at %d"%(a_files[x], a_files[i], absoluteCount)
                    imgADiff = ImageChops.difference(imgA2, imgA1)
                    imgADiffWeight = im2AWeight - im1AWeight

                    print "B: %s - %s at %d" % (b_files[x], b_files[i], absoluteCount)
                    imgBDiff = ImageChops.difference(imgB2, imgB1)
                    imgBDiffWeight = im2BWeight - im1BWeight

                    dist = '8_'

                    imNameA = 'img'+str(absoluteCount)+'_a_'+dist+str(imgADiffWeight).replace('.', 'd')+'.jpg'
                    imNameB = 'img'+str(absoluteCount)+'_b_'+dist+str(imgBDiffWeight).replace('.', 'd')+'.jpg'

                    imgADiff.save(outputFolder+imNameA)
                    imgBDiff.save(outputFolder+imNameB)

                    absoluteCount += 1

                x = i

            if a_files[i].split('_')[2] == '10':
                #print "--(10a)--> %s %d, %d"%(a_files[i], i, y)
                if not y == 0:
                    im1AWeight = float(a_files[y].split('_')[-1].replace('.jpg', '').replace('d', '.'))
                    im2AWeight = float(a_files[i].split('_')[-1].replace('.jpg', '').replace('d', '.'))
                    imgA1 = Image.open(inputFolder + a_files[y])
                    imgA2 = Image.open(inputFolder + a_files[i])

                    im1BWeight = float(b_files[y].split('_')[-1].replace('.jpg', '').replace('d', '.'))
                    im2BWeight = float(b_files[i].split('_')[-1].replace('.jpg', '').replace('d', '.'))
                    imgB1 = Image.open(inputFolder + b_files[y])
                    imgB2 = Image.open(inputFolder + b_files[i])

                    print "A: %s - %s at %d"%(a_files[y], a_files[i], absoluteCount)
                    imgADiff = ImageChops.difference(imgA2, imgA1)
                    imgADiffWeight = im2AWeight - im1AWeight

                    print "B: %s - %s at %d" % (b_files[y], b_files[i], absoluteCount)
                    imgBDiff = ImageChops.difference(imgB2, imgB1)
                    imgBDiffWeight = im2BWeight - im1BWeight

                    dist = '10_'

                    imNameA = 'img' + str(absoluteCount) + '_a_' + dist + str(imgADiffWeight).replace('.', 'd') + '.jpg'
                    imNameB = 'img' + str(absoluteCount) + '_b_' + dist + str(imgBDiffWeight).replace('.', 'd') + '.jpg'

                    imgADiff.save(outputFolder + imNameA)
                    imgBDiff.save(outputFolder + imNameB)

                    absoluteCount += 1
                y = i

            if a_files[i].split('_')[2] == '12':
                #print "--(12a)--> %s %d, %d"%(a_files[i], i, z)
                if not z == 0:
                    im1AWeight = float(a_files[z].split('_')[-1].replace('.jpg', '').replace('d', '.'))
                    im2AWeight = float(a_files[i].split('_')[-1].replace('.jpg', '').replace('d', '.'))
                    imgA1 = Image.open(inputFolder + a_files[z])
                    imgA2 = Image.open(inputFolder + a_files[i])

                    im1BWeight = float(b_files[z].split('_')[-1].replace('.jpg', '').replace('d', '.'))
                    im2BWeight = float(b_files[i].split('_')[-1].replace('.jpg', '').replace('d', '.'))
                    imgB1 = Image.open(inputFolder + b_files[z])
                    imgB2 = Image.open(inputFolder + b_files[i])

                    print "A: %s - %s at %d"%(a_files[z], a_files[i], absoluteCount)
                    imgADiff = ImageChops.difference(imgA2, imgA1)
                    imgADiffWeight = im2AWeight - im1AWeight

                    print "B: %s - %s at %d" % (b_files[z], b_files[i], absoluteCount)
                    imgBDiff = ImageChops.difference(imgB2, imgB1)
                    imgBDiffWeight = im2BWeight - im1BWeight

                    dist = '12_'

                    imNameA = 'img' + str(absoluteCount) + '_a_' + dist + str(imgADiffWeight).replace('.', 'd') + '.jpg'
                    imNameB = 'img' + str(absoluteCount) + '_b_' + dist + str(imgBDiffWeight).replace('.', 'd') + '.jpg'

                    imgADiff.save(outputFolder + imNameA)
                    imgBDiff.save(outputFolder + imNameB)

                    absoluteCount += 1
                z = i

# folderDiffsExtract('/Users/bregy/WebstormProjects/detechAlgorithm/cropped/','/Users/bregy/WebstormProjects/detechAlgorithm/diff/', tsub='t')