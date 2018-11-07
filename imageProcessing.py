import cv2
import numpy as np
from Element import Element


def getImage(name):
    return cv2.imread(name)


def showImage(name, image):
    cv2.imshow(name, image)


def makeCubes(image):
    height = image.shape[0]
    width = image.shape[1]

    if width % 9 != 0:
        width -= (width % 9)

    if height % 6 != 0:
        height -= (height % 6)

    image = cv2.resize(image, (width, height))

    cubeWidth = width // 9
    cubeHeight = height // 6

    cubes = []
    colors = ['blue', 'red', 'yellow', 'orange', 'white', 'green']

    for i in range(6):
        for j in range(9):
            content = image[i * cubeWidth:(i + 1) * cubeWidth - 1,
                                   j * cubeHeight:(j + 1) * cubeHeight - 1]
            cube = Element(colors[i], (i * 9) + j, content)
            cubes.append(cube)

    return cubes


def reassemblyImage(cubes):
    cubeContents = []

    for cube in cubes:
        cubeContents.append(cube.content)

    row1 = np.concatenate(cubeContents[0:9], axis=1)
    row2 = np.concatenate(cubeContents[9:18], axis=1)
    row3 = np.concatenate(cubeContents[18:27], axis=1)
    row4 = np.concatenate(cubeContents[27:36], axis=1)
    row5 = np.concatenate(cubeContents[36:45], axis=1)
    row6 = np.concatenate(cubeContents[45:54], axis=1)
    newImage = np.concatenate((row1, row2, row3, row4, row5, row6), axis=0)

    return newImage

def makeCubicFace(face):
    row1 = np.concatenate((face[0], face[1], face[2]), axis=1)
    row2 = np.concatenate((face[3], face[4], face[5]), axis=1)
    row3 = np.concatenate((face[6], face[7], face[8]), axis=1)

    newFace = np.concatenate((row1, row2, row3), axis=0)
    return newFace


def makeCubicCut(cubes):
    cubeContents = []

    for cube in cubes:
        cubeContents.append(cube.content)

    face1 = makeCubicFace(cubeContents[0:9])
    face2 = makeCubicFace(cubeContents[9:18])
    face3 = makeCubicFace(cubeContents[18:27])
    face4 = makeCubicFace(cubeContents[27:36])
    face5 = makeCubicFace(cubeContents[36:45])
    face6 = makeCubicFace(cubeContents[45:54])
    faceBlack = np.zeros((face1.shape[0], face1.shape[1], 3), np.uint8)

    row1 = np.concatenate((faceBlack, face1, faceBlack, faceBlack), axis=1)
    row2 = np.concatenate((face2, face3, face4, face5), axis=1)
    row3 = np.concatenate((faceBlack, face6, faceBlack, faceBlack), axis=1)

    newImage = np.concatenate((row1, row2, row3), axis=0)

    return newImage
