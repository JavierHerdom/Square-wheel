import numpy as np


def buildArray(solution):
    newSolution = list()
    f1 = list()
    f2 = list()
    f3 = list()
    f4 = list()
    f5 = list()
    f6 = list()
    f7 = list()
    for i in range(len(solution)):
        if i < 7:
            f1.append(solution[i])
        elif i >= 7 and i < 14:
            f2.append(solution[i])
        elif i >= 14 and i < 21:
            f3.append(solution[i])
        elif i >= 21 and i < 28:
            f4.append(solution[i])
        elif i >= 28 and i < 35:
            f5.append(solution[i])
        elif i >= 35 and i < 42:
            f6.append(solution[i])
        elif i >= 42 and i < 49:
            f7.append(solution[i])
    newSolution.append(f1)
    newSolution.append(f2)
    newSolution.append(f3)
    newSolution.append(f4)
    newSolution.append(f5)
    newSolution.append(f6)
    newSolution.append(f7)
    return newSolution


def rotAnd2dRoad(road):
    newRoadP1 = buildArray(road)
    rotated = np.rot90(newRoadP1)
    return rotated


def checkColumn(line, largo, min, max, nEspacios, roadList, count):
    if len(line) == largo and min <= count < max:
        for char in line:
            if char == " ":
                char = ""
            roadList.append(char)
        for i in range(0,nEspacios):
            roadList.append("")


def readFile(file):
    roadP1 = list()
    roadP2 = list()
    roadP3 = list()
    roadP4 = list()
    file = open(file, "r")
    count = 0
    for line in file:
        line = line.replace('\n'," ")
        #Road P1
        checkColumn(line, 4, 0, 7, 3, roadP1, count)
        checkColumn(line, 3, 0, 7, 4, roadP1, count)
        checkColumn(line, 2, 0, 7, 5, roadP1, count)
        checkColumn(line, 1, 0, 7, 6, roadP1, count)
        #Road P2
        checkColumn(line, 4, 7, 14, 3, roadP2, count)
        checkColumn(line, 3, 7, 14, 4, roadP2, count)
        checkColumn(line, 2, 7, 14, 5, roadP2, count)
        checkColumn(line, 1, 7, 14, 6, roadP2, count)
        #Road P3
        checkColumn(line, 4, 14, 21, 3, roadP3, count)
        checkColumn(line, 3, 14, 21, 4, roadP3, count)
        checkColumn(line, 2, 14, 21, 5, roadP3, count)
        checkColumn(line, 1, 14, 21, 6, roadP3, count)
        #Road P4
        checkColumn(line, 4, 21, 28, 3, roadP4, count)
        checkColumn(line, 3, 21, 28, 4, roadP4, count)
        checkColumn(line, 2, 21, 28, 5, roadP4, count)
        checkColumn(line, 1, 21, 28, 6, roadP4, count)
        count += 1

    newRoadP1 = rotAnd2dRoad(roadP1)
    newRoadP2 = rotAnd2dRoad(roadP2)
    newRoadP3 = rotAnd2dRoad(roadP3)
    newRoadP4 = rotAnd2dRoad(roadP4)
    return newRoadP1, newRoadP2, newRoadP3, newRoadP4


p1,p2,p3,p4 = readFile('road.txt')

print(f"Camino 1 : \n {p1}")
print(f"Camino 2 : \n {p2}")
print(f"Camino 3 : \n {p3}")
print(f"Camino 4 : \n {p4}")