import cv2
import ImageProcessing as IP
from collections import deque

scrambled_image = IP.get_image('scrambled.png')
scrambled_image = scrambled_image[:, :, 1]


def load_generate_vectors():
    with open('KeyH.txt') as f:
        height_vector = list(map(int, f.read().splitlines()))
    with open('KeyW.txt') as f:
        width_vector = list(map(int, f.read().splitlines()))

    vectors = [height_vector, width_vector]
    return vectors


def remove_scramble():
    my_vectors = load_generate_vectors()
    height_vector = my_vectors[0]
    width_vector = my_vectors[1]
    height = scrambled_image.shape[0]
    width = scrambled_image.shape[1]

    for i in range(width):
        elements_sum = 0
        for j in range(height):
            elements_sum += scrambled_image[j][i]

        shift_direction = elements_sum % 2

        if shift_direction != 0:
            shift = circular_shift(-width_vector[i], column(scrambled_image, i))
        else:
            shift = circular_shift(width_vector[i], column(scrambled_image, i))
        put_column(shift, i)

    for row in range(height):
        elements_sum = 0
        for row_elements in range(width):
            elements_sum += scrambled_image[row][row_elements]

        shift_length = elements_sum % 2
        if shift_length != 0:
            scrambled_image[row] = circular_shift(-height_vector[row], scrambled_image[row])
        else:
            scrambled_image[row] = circular_shift(height_vector[row], scrambled_image[row])


def put_column(shifted, column_number):
    height = scrambled_image.shape[0]

    for j in range(height):
        scrambled_image[j][column_number] = shifted[j]


def column(matrix, i):
    return [row[i] for row in matrix]


def circular_shift(shift_length, source_list):
    list_to_deque = deque(source_list)
    list_to_deque.rotate(shift_length)
    return list(list_to_deque)


remove_scramble()

IP.show_image("THis", scrambled_image)

cv2.waitKey(0)
