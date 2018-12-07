from random import randint
from math import pow
from collections import deque
import unittest
import ImageProcessing as iP
import cv2

image = iP.get_image("bpg_part.png")
#print(image.dtype)
image = image[:, :, 1]

#image = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

def generate_scrambling_vectors(height, width, image_bit_size):  # (1)
    height_vector, width_vector = [], []
    biggest_element = pow(2, image_bit_size)-1
    for i in range(height):
        height_vector.append(randint(0, biggest_element))
    for j in range(width):
        width_vector.append(randint(0, biggest_element))

    vectors = [height_vector, width_vector]

    return vectors

def vector_scrambling():
    height = image.shape[0]
    width = image.shape[1]
    generated_vectors = generate_scrambling_vectors(height, width, 8)
    height_vector = generated_vectors[0]
    width_vector = generated_vectors[1]
    with open("KeyH.txt", "w") as text_file:
        text_file.write('\n'.join(str(element) for element in height_vector))
    with open("KeyW.txt", "w") as text_file:
        text_file.write('\n'.join(str(element) for element in width_vector))

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
        put_column(shift, i)


def put_column(shifted, column_number):
    height = image.shape[0]

    for j in range(height):
        image[j][column_number] = shifted[j]

def column(matrix, i):
    return [row[i] for row in matrix]

#deque.rotate(n) for n > 0 - right, n < 0 - left
def circular_shift(shift_length, source_list):
    list_to_deque = deque(source_list)
    list_to_deque.rotate(shift_length)
    return list(list_to_deque)



class Test(unittest.TestCase):
    def test_vectors_not_empty(self):
        test = generate_scrambling_vectors(20, 30, 16)
        assert test[0] != 0
        assert test[1] != 0


#unittest.main()
vector_scrambling()

cv2.imwrite('scrambled.png', image)
cv2.imshow('My', image)
cv2.waitKey(0)
