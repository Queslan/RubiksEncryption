import cv2
import ImageProcessing as iP
from collections import deque


def load_generate_vectors():
    with open('KeyH.txt') as f:
        height_vector = list(map(int, f.read().splitlines()))
    with open('KeyW.txt') as f:
        width_vector = list(map(int, f.read().splitlines()))

    vectors = [height_vector, width_vector]
    return vectors


def remove_scramble(scrambled_image):
    for i in range(width):
        option = i % 2
        if option != 0:
            shift = xor_operation(column(scrambled_image, i), width_vector[i])
        else:
            shift = xor_operation(column(scrambled_image, i), rotated_width_vector[i])
        put_column(shift, i, scrambled_image)

    for row in range(height):
        option = row % 2
        if option != 0:
            scrambled_image[row] = xor_operation(scrambled_image[row], height_vector[row])
        else:
            scrambled_image[row] = xor_operation(scrambled_image[row], rotated_height_vector[row])

    for i in range(width):
        elements_sum = 0
        for j in range(height):
            elements_sum += scrambled_image[j][i]

        shift_direction = elements_sum % 2

        if shift_direction != 0:
            shift = circular_shift(-width_vector[i], column(scrambled_image, i))
        else:
            shift = circular_shift(width_vector[i], column(scrambled_image, i))
        put_column(shift, i, scrambled_image)

    for row in range(height):
        elements_sum = 0
        for row_elements in range(width):
            elements_sum += scrambled_image[row][row_elements]

        shift_length = elements_sum % 2
        if shift_length != 0:
            scrambled_image[row] = circular_shift(-height_vector[row], scrambled_image[row])
        else:
            scrambled_image[row] = circular_shift(height_vector[row], scrambled_image[row])


def put_column(shifted, column_number, scrambled_image):
    for j in range(height):
        scrambled_image[j][column_number] = shifted[j]


def column(matrix, i):
    return [row[i] for row in matrix]


def circular_shift(shift_length, source_list):
    list_to_deque = deque(source_list)
    list_to_deque.rotate(shift_length)
    return list(list_to_deque)


def get_image_color_channels():
    blue = image_og[:, :, 0]
    green = image_og[:, :, 1]
    red = image_og[:, :, 2]
    return blue, green, red


def remove_scramble_color_channels():
    remove_scramble(image_blue)
    remove_scramble(image_green)
    remove_scramble(image_red)


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


image_og = iP.get_image('scrambled.png')
image_blue, image_green, image_red = get_image_color_channels()

cv2.imshow("Scrambled image", image_og)

height = image_og.shape[0]
width = image_og.shape[1]
height_vector, width_vector = load_generate_vectors()
rotated_height_vector = list_180_rotation(height_vector)
rotated_width_vector = list_180_rotation(width_vector)
remove_scramble_color_channels()


iP.show_image("Scramble removed", image_og)

cv2.waitKey(0)
