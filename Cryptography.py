from collections import deque
from random import randint
import numpy as np


class Cryptography:
    image = None
    blue = None
    red = None
    green = None

    def __init__(self, image):
        self.image = image
        self.height = image.shape[0]
        self.width = image.shape[1]
        self.height_vector = []
        self.width_vector = []

    def split_color_channels(self):  # B G R
        self.blue = self.image[:, :, 0]
        self.green = self.image[:, :, 1]
        self.red = self.image[:, :, 2]

    def generate_scrambling_vectors(self, image_bit_size):
        biggest_element = pow(2, image_bit_size) - 1
        for i in range(self.height):
            self.height_vector.append(randint(0, biggest_element))
        for j in range(self.width):
            self.width_vector.append(randint(0, biggest_element))

        with open("KeyH.txt", "w") as text_file:
            text_file.write('\n'.join(str(element) for element in self.height_vector.copy()))
        with open("KeyW.txt", "w") as text_file:
            text_file.write('\n'.join(str(element) for element in self.width_vector.copy()))

    def load_generate_vectors(self):
        with open('KeyH.txt') as f:
            self.height_vector = list(map(int, f.read().splitlines()))
        with open('KeyW.txt') as f:
            self.width_vector = list(map(int, f.read().splitlines()))

    def xor_operation(self, source_list, vector_element):
        copy_to_return = source_list.copy()
        for i in range(len(copy_to_return)):
            copy_to_return[i] = copy_to_return[i] ^ vector_element
        return copy_to_return

    def change_current_image(self, image):
        self.image = image

    def rows_circular(self, scramble):
        for row in range(self.height):
            elements_sum = 0
            for row_elements in range(self.width):
                elements_sum += self.image[row][row_elements]
            shift_length = elements_sum % 2
            if not scramble:
                shift_length -= 1

            if shift_length != 0:
                self.image[row, :] = np.roll(self.image[row, :], self.height_vector[row])
            else:
                self.image[row, :] = np.roll(self.image[row, :], -self.height_vector[row])

    def columns_circular(self, scramble):
        for column in range(self.width):
            elements_sum = 0
            for j in range(self.height):
                elements_sum += self.image[j][column]

            shift_direction = elements_sum % 2
            if not scramble:
                shift_direction -= 1

            if shift_direction != 0:
                self.image[:, column] = np.roll(self.image[:, column], self.width_vector[column])
            else:
                self.image[:, column] = np.roll(self.image[:, column], -self.width_vector[column])

    def scramble(self):
        self.rows_circular(True)
        self.columns_circular(True)

    def un_scramble(self):
        self.columns_circular(False)
        self.rows_circular(False)

    def rows_xor_operation(self):
        for row in range(self.height):
            rotated_height_vector = self.height_vector[::-1]
            option = row % 2
            if option != 0:
                self.image[row, :] = self.xor_operation(self.image[row], self.height_vector[row])
            else:
                self.image[row, :] = self.xor_operation(self.image[row], rotated_height_vector[row])

    def columns_xor_operation(self):
        for column in range(self.width):
            rotated_width_vector = self.width_vector[::-1]
            option = column % 2
            if option != 0:
                self.image[:, column] = self.xor_operation(self.image[:, column], self.width_vector[column])
            else:
                self.image[:, column] = self.xor_operation(self.image[:, column], rotated_width_vector[column])

    def xor_encryption(self):
        self.rows_xor_operation()
        self.columns_xor_operation()

    def xor_decryption(self):
        self.columns_xor_operation()
        self.rows_xor_operation()
