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


def getFullImage(cubes):
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