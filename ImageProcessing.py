import cv2
import numpy as np
from Element import Element


def get_image(name):
    return cv2.imread(name, cv2.IMREAD_UNCHANGED)


def show_image(name, image):
    cv2.imshow(name, image)


def make_cubes(image):
    height = image.shape[0]
    width = image.shape[1]

    if width % 9 != 0:
        width -= (width % 9)

    if height % 6 != 0:
        height -= (height % 6)

    image = cv2.resize(image, (width, height))

    cube_width = width // 9
    cube_height = height // 6

    cubes = []
    colors = ['blue', 'red', 'yellow', 'orange', 'white', 'green']

    for i in range(6):
        for j in range(9):
            content = image[i * cube_width:(i + 1) * cube_width - 1,
                                   j * cube_height:(j + 1) * cube_height - 1]
            cube = Element(colors[i], (i * 9) + j, content)
            cubes.append(cube)

    return cubes


def reassembly_image(cubes):
    cube_contents = []

    for cube in cubes:
        cube_contents.append(cube.content)

    row1 = np.concatenate(cube_contents[0:9], axis=1)
    row2 = np.concatenate(cube_contents[9:18], axis=1)
    row3 = np.concatenate(cube_contents[18:27], axis=1)
    row4 = np.concatenate(cube_contents[27:36], axis=1)
    row5 = np.concatenate(cube_contents[36:45], axis=1)
    row6 = np.concatenate(cube_contents[45:54], axis=1)
    new_image = np.concatenate((row1, row2, row3, row4, row5, row6), axis=0)

    return new_image


def make_cubic_face(face):
    row1 = np.concatenate((face[0], face[1], face[2]), axis=1)
    row2 = np.concatenate((face[3], face[4], face[5]), axis=1)
    row3 = np.concatenate((face[6], face[7], face[8]), axis=1)

    new_face = np.concatenate((row1, row2, row3), axis=0)
    return new_face


def make_cubic_cut(cubes):
    cube_contents = []

    for cube in cubes:
        cube_contents.append(cube.content)

    face1 = make_cubic_face(cube_contents[0:9])
    face2 = make_cubic_face(cube_contents[9:18])
    face3 = make_cubic_face(cube_contents[18:27])
    face4 = make_cubic_face(cube_contents[27:36])
    face5 = make_cubic_face(cube_contents[36:45])
    face6 = make_cubic_face(cube_contents[45:54])
    face_black = np.zeros((face1.shape[0], face1.shape[1], 3), np.uint8)

    row1 = np.concatenate((face_black, face1, face_black, face_black), axis=1)
    row2 = np.concatenate((face2, face3, face4, face5), axis=1)
    row3 = np.concatenate((face_black, face6, face_black, face_black), axis=1)

    newImage = np.concatenate((row1, row2, row3), axis=0)

    return newImage
