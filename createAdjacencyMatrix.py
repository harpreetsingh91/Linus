from tables import *
import numpy as np
import json
import pickle


readVectorFile = json.load(open("songVectorsFileJSONwithTimbres.txt"))

def euclDist(a):
    dis = 0
    for value in a:
        dis += (value*value)
    return math.sqrt(dis)

D = 3 # D defined as 2
alpha = 11000 #alpha defined as a big value
adjacencyMatrix = []
for i in range(0,10000):
    iData = readVectorFile[str(i)][1] #since vector data is at position 1
    adjacencyRow = []
    for j in range(0,10000):
        jData = readVectorFile[str(j)][1]
        #add lists instead of appending
        temp = sum(abs(np.array(iData)-np.array(jData)))
        if (temp<D):
            adjacencyRow += [temp]
        else:
            adjacencyRow += [alpha]
    adjacencyMatrix.append(adjacencyRow)
    print i


#save to disk
npAdjacenyMatrix = np.array(adjacencyMatrix)




amHDF = openFile('adjacencyMatrixWithTimbres.hdf', 'w')
atom = Atom.from_dtype(npAdjacenyMatrix.dtype)
filters = Filters(complib='blosc', complevel=2)
ds = amHDF.createCArray(amHDF.root, 'adjacencyMatrix', atom, npAdjacenyMatrix.shape, filters=filters)
ds[:] = npAdjacenyMatrix
amHDF.close()
