def folderDetech2tags(input_path, output_path):
    files = [f for f in listdir(input_path) if isfile(join(input_path, f))]
    files = [f for f in files if 'detech' in f]

    filesp = [f.split('detechPhoto') for f in files]
    filesp = [[int(f[0]), datetime.strptime(f[1].replace('.jpg', ''), '%Y%m%d%H%M%S')] for f in filesp]
    filesp = sorted(filesp, key=lambda fi: fi[0])

    dist = ['8', '10', '12']
    finalNames = []
    typehand = 0

    a_hand = []
    b_hand = []

    totalSeconds = float((filesp[-1][1] - filesp[0][1]).seconds)

    psc = 0
    for i in range(1,filesp[-1][0]+1):
        j = i-1
        for m in range(3):
            if j%6==m:
                a_hand.append(filesp[j])
                hand = 'a'
                num = (filesp[j][1]-filesp[0][1]).seconds
                w = 0.
                if num!=0:
                    w = num/totalSeconds

                fname = 'img'+str(filesp[j][0])+'_'+hand+'_'+dist[m]+'_'+str(w).replace('.', 'd') + '.jpg'
                finalNames.append(fname)

        f = filesp[j]
        if not f in a_hand:
            hand = 'b'
            den = (filesp[j][1]-filesp[0][1]).seconds
            w = 0
            if num!=0:
                w = num/totalSeconds
            fname = 'img'+str(filesp[j][0])+'_'+hand+'_'+dist[psc]+'_'+str(w).replace('.', 'd') + '.jpg'
            if psc == 2:
                psc = 0 
            else:
                psc = psc + 1

            finalNames.append(fname)
        
    files_names = sorted([[int(f.split('detechPhoto')[0]), f] for f in files], key=lambda r:r[0])
    files_names = [f[1] for f in files_names]
    
    if len(files_names) == len(finalNames) :
        if input_path[-1] != '/':
            input_path = input_path + '/'
        if output_path[-1] != '/':
            output_path = output_path + '/'

        for i in range(len(files_names)):
            copyfile(input_path + files_names[i], output_path + finalNames[i])
