def differenceIm_crop(path, distancia):
    from os import listdir
    import os
    import cv2
    #import matplotlib.pyplot as plt
    from uppselector import launchUIForSelection

    onlyfiles = [f for f in listdir(path + "D" + distancia + "_Rigido/")]
    entro_a = 0
    entro_b = 0


    path = path + "/" + "Diferencias" + distancia

    if not os.path.exists(path):
        os.makedirs(path)
    path_a = path + "/" + "Dif_a"
    path_b = path + "/" + "Dif_b"
    if not os.path.exists(path_a):
        os.makedirs(path_a)
    if not os.path.exists(path_b):
        os.makedirs(path_b)


    path = path.split("/Diferencias")[0]

    list_a = []
    list_b = []
    split_nom_a = []
    split_nom_b = []

    for i in range(0, len(onlyfiles)):
        im_nom = onlyfiles[i]

        if "a" in im_nom and distancia in im_nom:
            nom_a = im_nom.split(".jpg")[0]
            nom_a = nom_a.split("d")[1]
            split_nom_a.append(nom_a)
            entro_a += 1
            list_a.append(im_nom)

        if "b" in im_nom and distancia in im_nom:
            nom_b = im_nom.split(".jpg")[0]
            nom_b = nom_b.split("d")[1]
            split_nom_b.append(nom_b)
            entro_b += 1
            list_b.append(im_nom)

    l = [list(x) for x in zip(list_a, split_nom_a)]
    list_a = sorted(l, key=lambda r:r[1])


    l = [list(x) for x in zip(list_b, split_nom_b)]
    list_b = sorted(l, key=lambda r: r[1])

    l_a = []
    l_b = []
    for i in range(0,len(list_a)):
        l_a.append(list_a[i][0])
    for i in range(0,len(list_b)):
        l_b.append(list_b[i][0])

    list_a = l_a
    list_b = l_b

    points = launchUIForSelection(path + "D" + distancia + "_Rigido/" + list_a[0])
    p1 = points.get('p0')
    p2 = points.get('p1')
    p1x = int(p1[0])
    p2x = int(p2[0])
    p1y = int(p1[1])
    p2y = int(p2[1])



    import matplotlib.pyplot as plt
    for i in range(0, len(list_a)-1):
        im1 = cv2.imread(path + "D" + distancia + "_Rigido/" + list_a[i])
        im2 = cv2.imread(path + "D" + distancia + "_Rigido/" + list_a[i+1])
        new_im = im2[p1y:p2y,p1x:p2x] - im1[p1y:p2y,p1x:p2x]
        imfile = "imagen" + str(i) + ".jpg"
        cv2.imwrite(path + "Diferencias" + distancia + "/Dif_a/" + imfile, abs(new_im))
        # print("Elementos a "), print(i)

    for i in range(0, len(list_b)-1):
        im1 = cv2.imread(path + "D" + distancia + "_Rigido/" + list_b[i])
        im2 = cv2.imread(path + "D" + distancia + "_Rigido/" + list_b[i+1])
        new_im = im2[p1y:p2y,p1x:p2x] - im1[p1y:p2y,p1x:p2x]
        imfile = "imagen" + str(i) + ".jpg"
        cv2.imwrite(path + "Diferencias" + distancia + "/Dif_b/" + imfile, abs(new_im))
        # print("Elementos b "), print(i)

'''
Total Images without crop
'''
def differenceIm_all(path, distancia):
    from os import listdir
    import os
    import cv2
    # import matplotlib.pyplot as plt

    onlyfiles = [f for f in listdir(path + "D" + distancia + "_Rigido/")]
    entro_a = 0
    entro_b = 0

    path = path + "/" + "Diferencias_Im" + distancia

    if not os.path.exists(path):
        os.makedirs(path)
    path_a = path + "/" + "Dif_Imsabs"
    if not os.path.exists(path_a):
        os.makedirs(path_a)

    path = path.split("/Diferencias_Im")[0]

    list_a = []
    list_b = []
    split_nom_a = []
    split_nom_b = []

    for i in range(0, len(onlyfiles)):
        im_nom = onlyfiles[i]

        if "a" in im_nom and distancia in im_nom:
            nom_a = im_nom.split(".jpg")[0]
            nom_a = nom_a.split("d")[1]
            split_nom_a.append(nom_a)
            entro_a += 1
            list_a.append(im_nom)

        if "b" in im_nom and distancia in im_nom:
            nom_b = im_nom.split(".jpg")[0]
            nom_b = nom_b.split("d")[1]
            split_nom_b.append(nom_b)
            entro_b += 1
            list_b.append(im_nom)

    l = [list(x) for x in zip(list_a, split_nom_a)]
    list_a = sorted(l, key=lambda r: r[1])

    l = [list(x) for x in zip(list_b, split_nom_b)]
    list_b = sorted(l, key=lambda r: r[1])

    l_a = []
    l_b = []
    for i in range(0, len(list_a)):
        l_a.append(list_a[i][0])
    for i in range(0, len(list_b)):
        l_b.append(list_b[i][0])

    list_a = l_a
    list_b = l_b

    for i in range(0, len(list_a)):
        im1 = cv2.imread(path + "D" + distancia + "_Rigido/" + list_a[i])
        im2 = cv2.imread(path + "D" + distancia + "_Rigido/" + list_b[i])
        new_im = im2 - im1
        imfile = "imagen" + str(i) + ".jpg"
        cv2.imwrite(path + "Diferencias_Im" + distancia + "/Dif_Imsabs/" + imfile, abs(new_im))