from __future__ import division
from __future__ import print_function

import os
import numpy as np

class DetechDataset:

    def __init__(self, data, trainPercent):
        self.raw_data = data
        cutting = int(len(data)*trainPercent)
        self.train = data[0:cutting]
        self.test = data[cutting:-1]

    def next_batch(self, size):
        np.random.shuffle(self.train)
        batch = self.train[0:size]
        x = np.array([b[0] for b in batch])
        y = np.array([[b[1]] for b in batch])
        return x, y

    def next_batch_one_hot(self, size):
        np.random.shuffle(self.train)
        batch = self.train[0:size]
        x = np.array([b[0] for b in batch])
        binaryOneHot = []
        for b in batch:
            out = b[1]
            if 0<=out<1/4:
                binaryOneHot.append(1)
                continue
            if 1/4<=out<2/4:
                binaryOneHot.append(2)
                continue
            if 2/4<=out<3/4:
                binaryOneHot.append(4)
                continue
            if 3/4<=out<1:
                binaryOneHot.append(8)
                continue
        ohStrings = ['{0:04b}'.format(oh) for oh in binaryOneHot]

        y = np.asarray([[int(s[0]), int(s[1]), int(s[2]), int(s[3])] for s in ohStrings])
        return x, y

    def get_test_data(self):
        x = np.array([b[0] for b in self.test])
        binaryOneHot = []
        for b in self.test:
            out = b[1]
            if 0 <= out < 1 / 4:
                binaryOneHot.append(1)
                continue
            if 1 / 4 <= out < 2 / 4:
                binaryOneHot.append(2)
                continue
            if 2 / 4 <= out < 3 / 4:
                binaryOneHot.append(4)
                continue
            if 3 / 4 <= out < 1:
                binaryOneHot.append(8)
                continue
        ohStrings = ['{0:04b}'.format(oh) for oh in binaryOneHot]

        y = np.asarray([[int(s[0]), int(s[1]), int(s[2]), int(s[3])] for s in ohStrings])
        return x, y

def read_data_sets(path):
    filenames = [f for f in os.listdir(path)]

    finalData = []
    for f in filenames:
        dataPath = os.path.join(path, f)
        data = np.load(dataPath)
        finalData.append(data)

    return DetechDataset(finalData, .75)

