from random import randint
import numpy as np
import ImageProcessing as iP

class Cryptography:
    blue = None
    red = None
    green = None

    def __init__(self, path):
        image = iP.get_image(path)
        self.main_image = image
        self.image = image
        self.height = image.shape[0]
        self.width = image.shape[1]
        self.vector_height = []
        self.vector_width = []
        self.modulo_row = 0
        self.modulo_column = 0
        self.rotated_height_vector = []
        self.rotated_width_vector = []

    def split_color_channels(self):  # B G R
        self.blue = self.image[:, :, 0]
        self.green = self.image[:, :, 1]
        self.red = self.image[:, :, 2]

    def set_image_to_blue_channel(self):
        self.change_current_image(self.blue)

    def set_image_to_green_channel(self):
        self.change_current_image(self.green)

    def set_image_to_red_channel(self):
        self.change_current_image(self.red)

    def equalize_all_channels(self):
        self.red = 0
        self.green = 0

    @staticmethod
    def check_if_gray_color(image):
        if np.all(image[:, :, 0] == image[:, :, 1]) and np.all(image[:, :, 1] == image[:, :, 2]):
            return True
        return False

    def generate_scrambling_vectors(self):
        image_type = self.image.dtype
        image_bit_size = 16 if image_type is np.dtype('uint16') else 8
        biggest_element = pow(2, image_bit_size) - 1
        for i in range(self.height):
            self.vector_height.append(randint(0, biggest_element))
        for j in range(self.width):
            self.vector_width.append(randint(0, biggest_element))

        with open("key/Ww.txt", "w") as text_file:
            text_file.write('\n'.join(str(element) for element in self.vector_height.copy()))
        with open("key/Ws.txt", "w") as text_file:
            text_file.write('\n'.join(str(element) for element in self.vector_width.copy()))
        self.set_scramble_modulo()

    def load_generate_vectors(self):
        with open('key/Ww.txt') as f:
            self.vector_height = list(map(int, f.read().splitlines()))
        with open('key/Ws.txt') as f:
            self.vector_width = list(map(int, f.read().splitlines()))
        self.set_scramble_modulo()

    def change_current_image(self, image):
        self.image = image

    def set_scramble_modulo(self):
        self.modulo_row = self.generate_scramble_modulo(self.vector_height)
        self.modulo_column = self.generate_scramble_modulo(self.vector_width)

    def generate_scramble_modulo(self, vector):
        return ((vector[0]+vector[self.height-1])*vector[self.height//2]) % self.height + 100

    def column_scramble(self, scramble, column):
        elements_sum = 0
        for j in range(self.height):
            elements_sum += self.image[j][column]
        modulo_shift_column = elements_sum % self.modulo_column
        shift_direction = modulo_shift_column % 2
        if not scramble:
            shift_direction -= 1
        if shift_direction == 0:
            self.image[:, column] = np.roll(self.image[:, column], -modulo_shift_column)
        else:
            self.image[:, column] = np.roll(self.image[:, column], modulo_shift_column)

    def row_scramble(self, scramble, row):
        elements_sum = 0
        for row_elements in range(self.width):
            elements_sum += self.image[row][row_elements]

        modulo_shift_row = elements_sum % self.modulo_row

        shift_direction = modulo_shift_row % 2
        if not scramble:
            shift_direction -= 1
        if shift_direction == 0:
            self.image[row, :] = np.roll(self.image[row, :], modulo_shift_row)
        else:
            self.image[row, :] = np.roll(self.image[row, :], -modulo_shift_row)

    def circular_scramble_alternate(self):
        number_of_iterations = self.generate_number_of_iterations()
        start_option = (self.vector_height[0] + self.vector_width[0]) % 2
        for j in range(number_of_iterations):
            for i in range(self.width):
                if start_option == 0:
                    self.row_scramble(True, i)
                    self.column_scramble(True, i)
                else:
                    self.column_scramble(True, i)
                    self.row_scramble(True, i)

    def circular_un_scramble_alternate(self):
        number_of_iterations = self.generate_number_of_iterations()
        start_option = (self.vector_height[0] + self.vector_width[0]) % 2
        for j in range(number_of_iterations):
            for i in range(self.width-1, -1, -1):
                if start_option != 0:
                    self.row_scramble(False, i)
                    self.column_scramble(False, i)
                else:
                    self.column_scramble(False, i)
                    self.row_scramble(False, i)

    def generate_number_of_iterations(self):
        return ((self.vector_height[0]+self.vector_height[self.height//2]) *
                (self.vector_width[0]+self.vector_width[self.width//2])) % 4 + 2

    @staticmethod
    def xor_operation(source_list, vector_element):
        copy_to_return = source_list.copy()
        for i in range(len(copy_to_return)):
            copy_to_return[i] = copy_to_return[i] ^ vector_element
        return copy_to_return

    def rows_xor_operation(self, row):
        rotated_height_vector = self.vector_height[::-1]
        option = row % 2
        if option != 0:
            self.image[row, :] = self.xor_operation(self.image[row], self.vector_height[row])
        else:
            self.image[row, :] = self.xor_operation(self.image[row], rotated_height_vector[row])

    def columns_xor_operation(self, column):
        rotated_width_vector = self.vector_width[::-1]
        option = column % 2
        if option != 0:
            self.image[:, column] = self.xor_operation(self.image[:, column], self.vector_width[column])
        else:
            self.image[:, column] = self.xor_operation(self.image[:, column], rotated_width_vector[column])


    def xor_encryption(self):
        start_option = (self.vector_height[0] + self.vector_width[0]) % 2
        for i in range(self.height):
            if start_option == 0:
                self.rows_xor_operation(i)
                self.columns_xor_operation(i)
            else:
                self.columns_xor_operation(i)
                self.rows_xor_operation(i)

    def xor_decryption(self):
        start_option = (self.vector_height[0] + self.vector_width[0]) % 2
        for i in range(self.height):
            if start_option != 0:
                self.rows_xor_operation(i)
                self.columns_xor_operation(i)
            else:
                self.columns_xor_operation(i)
                self.rows_xor_operation(i)

