import random
import sys
import string
import math
import array
import itertools
import operator
import collections
import os

# read the dataset
# def reading():
#     inputs = [];
#     for line in sys.stdin:
#         inputs.append(line[:-1]);
#     return inputs

def read(path,mapa):
    inputs = []
    archivo = open(path+mapa, "r")
    for line in archivo.readlines():
        if line[-1] == '\n':
            if line[0]!='s':
                inputs.append('s'+line[:-1])
            else:
                inputs.append(line[:-1])
        else:
            if line[0]!='s':
                inputs.append('s'+line[:-1])
            else:
                inputs.append(line[:-1])
    
    if inputs[-1][1] != 's':
        length = len(inputs[-1])
        line = 's'*length
        inputs.append(line)

    for i in inputs:
        print i

    return inputs

def obtainPaths(path):
    mapas = []
    for root, dirs, files in os.walk(path):
        for file in files[1:]:
            mapas.append(file)
    mapas = sorted(mapas, key=lambda mapa:int(mapa[6:-4]))
    return mapas

def unicTiles(uT,lowTiles):
    for line in lowTiles:
        for character in line:
            if not character in uT:
                uT.append(character)
    return uT

def splitMaps(mapa, splitNumber):
    splitMap = []
    splitsAux = []
    start = 0
    length = len(mapa) / splitNumber
    limit = length

    for index in xrange(0,splitNumber):
        if limit <= len(mapa) and limit+length <= len(mapa):
            splitsAux = mapa[start:limit]
            start = limit
            limit = start+length
        
        else:
            limit = len(mapa)
            splitsAux = mapa[start:limit]

        splitMap.append(splitsAux)

    return splitMap

def networkStructure(tipo):
    return -1

def createMatrix(unicTiles):
    m = [ [0 for x in range(len(unicTiles))] for y in range(len(unicTiles))]
    # for i,mi in enumerate(m):
    #     print i, mi
    #     print '\n'
    return m

def createMatrixNetwork3(unicTiles):
    m = [[{"sss":0}] for y in range(len(unicTiles))]
    # for i,mi in enumerate(m):
    #     for j,mii in enumerate(mi):
    #         print j,mii
    #     print '\n'
    return m

def fillMatrixNetwork3(mapa,matrix,unicTiles):
    m = []
    for i,line in enumerate(mapa):
        if i+1 < len(mapa):
            for prevC,actualC,diagC,botC in zip(line[0:],line[1:],mapa[i+1][0:],mapa[i+1][1:]):
                key = prevC+diagC+botC
                # print actualC,":",prevC,diagC,botC, '\n'
                index = unicTiles.index(actualC)
                # matrix[index][0]["ssM"] = 1
                if key in matrix[index][0]:
                    matrix[index][0][key] += 1
                    # print index
                else:
                    matrix[index][0][key] = 1
                    # print index
    # for m in matrix:
    #     print m
    return matrix

def fillProbabilityMatrixNetwork3(matrix,unicTiles):
    total = 0
    unicTilesTotal = []
    unicTotal = []
    
    for m in matrix:
        for uti in m:
            for i,j in uti.iteritems():
                total += j
            unicTotal.append(total)
            total = 0
    
    for i,m in enumerate(matrix):
        for uti in m:
            for key,val in uti.iteritems():
                if unicTotal[i] > 0:
                    uti[key] = float(val)/unicTotal[i]

    for m in matrix:
        print m

    return matrix

def garantizeSum(probabilities):
    # Garantize that the sum is equal to 1 or an aproximatly
    for nextC in probabilities:
        for previousC in nextC:
            total += previousC
        unicTotal.append(total)
        total = 0

    if all(unicTotal[0] == item for unics in unicTotal):
        return true
    return false

def fillMatrix(mapa,matrix,unicTiles):
    if mapa[-1][1] == 's':
        for line in mapa[:-1]:
            for previousC,nextC in zip(line[0:],line[1:]):
                indexP = unicTiles.index(previousC)
                indexN = unicTiles.index(nextC)
                matrix[indexN][indexP] += 1
    else:
        for line in mapa:
            for previousC,nextC in zip(line[0:],line[1:]):
                indexP = unicTiles.index(previousC)
                indexN = unicTiles.index(nextC)
                matrix[indexN][indexP] += 1
    
    return matrix 

def fillProbabilityMatrix(matrix,unicTiles):
    pM = createMatrix(unicTiles)
    createMatrixNetwork3(unicTiles);
    total = 0
    unicTilesTotal = []
    unicTotal = []

    # Obtain the total per each line
    for i in xrange(len(matrix)):
        for nextC in matrix:
            total += nextC[i]
        unicTilesTotal.append(total)
        total = 0

    # Get the probability of each value
    for i in xrange(len(matrix)):
        for iN,nextC in enumerate(matrix):
            if unicTilesTotal[i] != 0:
                pM[iN][i] = float(matrix[iN][i])/unicTilesTotal[i]
    return pM

def training(path,mapas,uT, splitNumber):
    probabilities = [None]*splitNumber
    probabilities2 = [None]*splitNumber
    m = [None] * splitNumber
    m2 = [None] * splitNumber
    splitM = []
    
    for mapa in mapas:
        input_data = read(path,mapa)
        unicTiles(uT,input_data)
        splitM.append(splitMaps(input_data, splitNumber))
    
    for i in xrange(0,splitNumber):
        m[i] = createMatrix(uT)
        m2[i]= createMatrixNetwork3(uT)

    for mapa in splitM:
        for i,sM in enumerate(mapa):
            fillMatrix(sM, m[i], uT)
            fillMatrixNetwork3(sM,m2[i],uT)
            # for mi in m[i]:
            #     print mi
            # print '\n'
            probabilities[i] = fillProbabilityMatrix(m[i],uT)
            probabilities2[i] = fillProbabilityMatrixNetwork3(m2[i],uT);

    return probabilities2

def nextMap(mapas):
    mapa =  mapas[-1]
    # print mapa[6:-4]
    number = int(mapa[6:-4])+1
    # print number
    
    if number > 10:
        mapa = mapa[:-6]+str(number)+".txt"
        # print mapa
    else:
        mapa = mapa[:-5]+str(number)+".txt"
    return mapa

def getMaxProbability(index,probabilities):
    maxProbabilities = []
    maxP = 0
    nextI = 0
    ind = 0
    
    for i,probability in enumerate(probabilities):
        if probability[index] > maxP:
            maxProbabilities.append(i)
            maxP = probability[index]
            ind = i

    # rI = random.randint(0,len(maxProbabilities)-1)
    # nextI = maxProbabilities[rI]
    return ind

def deleteContent(pfile):
    pfile.seek(0)
    pfile.truncate()

def getMaxProbabilityNetwork3(key,probabilities):
    maxP = 0
    ind = 0

    for lisT in probabilities:
        for i,dic in enumerate(lisT):
            if key in dic[0]:
                val = dic[0][key]
                if val > maxP:
                    ind = i
                    maxP = val
    return ind

def writingRecursionNetwork3(path,mapa,limitFile,limitColumn, probabilities, uT):
    newMap = []

    if limitFile-1 >= 0:
        for i in range(limitFile-1):
            newMap.append('s')

        print "prev", limitFile-1,limitColumn
        print "diag", limitFile, limitColumn
        print "bot", limitFile,limitColumn+1

        prevC = mapa[limitFile-1][limitColumn]
        diagC = mapa[limitFile][limitColumn]
        botC = mapa[limitFile][limitColumn+1]

        key = prevC+diagC+botC
        nextI = getMaxProbabilityNetwork3(key,probabilities)
        nextC = uT[nextI]

        nextString = mapa[limitFile-1]+nextC
        newMap.append(nextString);
        
        if limitFile < len(mapa)-1:
            for i in xrange(limitFile,len(mapa)):
                nextString = mapa[i]
                newMap.append(nextString)
        else:
            nextString = mapa[limitFile]
            newMap.append(nextString)
        
        if limitColumn == len(mapa[limitFile])-2 and limitFile == 1:
            # deleteContent(file)
            for nm in newMap:
                print nm
            #     file.write(nm+'\n')

        if limitColumn+1 < 4:
            print "column +1"
            writingRecursionNetwork3(path,newMap,limitFile,limitColumn+1,probabilities,uT)
        else:
            print "fila -1 column 0"
            writingRecursionNetwork3(path,newMap,limitFile-1,0,probabilities,uT)


        # file.close()/

def writingMapNetwork3(path, mapa, uT, probabilities, splitNumber):
    file = open(path+mapa, "w+")
    newMap = []
    nextI = []
    data = []

    rH = 4
    rW = 5

    for i in range(0,rH):
        file.write("s\n")
    for j in range(0,rW):
        file.write("s")

        last_line = 's' * rW

    file = open(path+mapa, "w+")

    for line in file.readlines():
        if line[-1] == '\n':
            data.append(line[:-1])
        else:
            data.append(line)

    sMaps = splitMaps(data,splitNumber)

    # Get the next characters
    for i,sM in enumerate(sMaps):
        if i <= splitNumber-1:
            newMap = writingRecursionNetwork3(path+mapa,sM,len(sM)-1,0, probabilities, uT)



def writingMap(path, mapa, uT, probabilities, splitNumber):
    file = open(path+mapa, "w+")
    newMap = []
    nextI = []
    data = []

    # put sentinels
    # rH =  random.randint(11,14)
    # rW =  random.randint(150,201)
    rH = 4
    rW = 5
    for i in range(0,rH):
        file.write("s\n")
    for j in range(0,rW):
        file.write("s")

        last_line = 's' * rW

    # put the rest of the characteres
    for h in xrange(0,rW-1):
        file = open(path+mapa, "w+")

        for line in file.readlines():
            data.append(line[:-1])

        sMaps = splitMaps(data,splitNumber)

        for i,sM in enumerate(sMaps):
            if i < splitNumber-1:
                for line in sM:
                    character = line[-1]
                    if character in uT:
                        index = uT.index(character)
                        nextI = getMaxProbability(index, probabilities[i])
                        nextString = line + uT[nextI] + '\n'
                        newMap.append(nextString)
            else:
                for line in sM[:-1]:
                    character = line[-1]
                    if character in uT:
                        index = uT.index(character)
                        nextI = getMaxProbability(index, probabilities[i])
                        # print character, uT[index],nextI, uT[nextI];
                        nextString = line + uT[nextI] + '\n'
                        newMap.append(nextString)
                newMap.append(last_line)

        deleteContent(file)
        for nM in newMap:
            file.write(nM)

        data = []
        newMap = []

    file.close

def sampling(path,mapas,uT, probabilities, splitNumber):
    mapa = nextMap(mapas)
    # writingMap(path, mapa, uT, probabilities, splitNumber)
    writingMapNetwork3(path,mapa,uT,probabilities,splitNumber)


def main():
    path = '/Users/Cr1s/Documents/Tesis/VGLC/'
    mapas = obtainPaths(path)
    
    uT = []
    splitNumber = 1
    probabilities = training(path,mapas,uT, splitNumber)
    # print '\n'
    # for i,p in enumerate(probabilities):
    #     for pi in p:
    #         print i, pi
    #     print '\n'

    sampling(path,mapas,uT, probabilities,splitNumber)


if __name__ == "__main__":
    main()