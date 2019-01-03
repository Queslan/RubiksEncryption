from random import randint
from math import pow
from collections import deque
import ImageProcessing as iP
import cv2


def generate_scrambling_vectors(image_bit_size):
    height_vector, width_vector = [], []
    biggest_element = pow(2, image_bit_size)-1
    for i in range(height):
        height_vector.append(randint(0, biggest_element))
    for j in range(width):
        width_vector.append(randint(0, biggest_element))

    with open("KeyH.txt", "w") as text_file:
        text_file.write('\n'.join(str(element) for element in height_vector))
    with open("KeyW.txt", "w") as text_file:
        text_file.write('\n'.join(str(element) for element in width_vector))

    vectors = [height_vector, width_vector]
    return vectors


def vector_scrambling(image):
    for row in range(height):
        elements_sum = 0
        for row_elements in range(width):
            elements_sum += image[row][row_elements]

        shift_length = elements_sum % 2
        if shift_length != 0:
            image[row] = circular_shift(height_vector[row], image[row])
        else:
            image[row] = circular_shift(-height_vector[row], image[row])

    for i in range(width):
        elements_sum = 0
        for j in range(height):
            elements_sum += image[j][i]

        shift_direction = elements_sum % 2

        if shift_direction != 0:
            shift = circular_shift(width_vector[i], column(image, i))
        else:
            shift = circular_shift(-width_vector[i], column(image, i))
        put_column(shift, i, image)

    for row in range(height):
        option = row % 2
        if option != 0:
            image[row] = xor_operation(image[row], height_vector[row])
        else:
            image[row] = xor_operation(image[row], rotated_height_vector[row])

    for i in range(width):
        option = i % 2
        if option != 0:
            shift = xor_operation(column(image, i), width_vector[i])
        else:
            shift = xor_operation(column(image, i), rotated_width_vector[i])
        put_column(shift, i, image)


def put_column(shifted, column_number, image):
    for j in range(height):
        image[j][column_number] = shifted[j]


def column(matrix, i):
    return [row[i] for row in matrix]


def list_180_rotation(source_list):
    list_to_deque = deque(source_list)
    list_size = len(source_list)
    list_to_deque.rotate(list_size)
    return list(list_to_deque)


def xor_operation(source_list, vector_element):
    copy_to_return = source_list.copy()
    for element in copy_to_return:
         element = element ^ vector_element
    return copy_to_return



def circular_shift(shift_length, source_list):  # deque.rotate(n) for n > 0 - right, n < 0 - left
    list_to_deque = deque(source_list)
    list_to_deque.rotate(shift_length)
    return list(list_to_deque)


def scramble_color_channels():
    vector_scrambling(image_blue)
    vector_scrambling(image_green)
    vector_scrambling(image_red)


def get_image_color_channels():  # B G R
    blue = image_og[:, :, 0]
    green = image_og[:, :, 1]
    red = image_og[:, :, 2]
    return blue, green, red


image_og = iP.get_image("bpg_part.png")
image_blue, image_green, image_red = get_image_color_channels()
cv2.imshow("Before scramble", image_og)

height = image_og.shape[0]
width = image_og.shape[1]
height_vector, width_vector = generate_scrambling_vectors(8)
rotated_height_vector = list_180_rotation(height_vector)
rotated_width_vector = list_180_rotation(width_vector)
scramble_color_channels()


cv2.imwrite('scrambled.png', image_og)
cv2.imshow('After scramble', image_og)
cv2.waitKey(0)
