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
        self.vector_height = []
        self.vector_width = []
        self.modulo_row = 0
        self.modulo_column = 0

    def split_color_channels(self):  # B G R
        self.blue = self.image[:, :, 0]
        self.green = self.image[:, :, 1]
        self.red = self.image[:, :, 2]

    def generate_scrambling_vectors(self):
        image_type = self.image.dtype
        image_bit_size = 16 if image_type is np.dtype('uint16') else 8
        biggest_element = pow(2, image_bit_size) - 1
        for i in range(self.height):
            self.vector_height.append(randint(0, biggest_element))
        for j in range(self.width):
            self.vector_width.append(randint(0, biggest_element))

        with open("Ww.txt", "w") as text_file:
            text_file.write('\n'.join(str(element) for element in self.vector_height.copy()))
        with open("Ws.txt", "w") as text_file:
            text_file.write('\n'.join(str(element) for element in self.vector_width.copy()))

        self.set_scramble_modulo()

    def load_generate_vectors(self):
        with open('Ww.txt') as f:
            self.vector_height = list(map(int, f.read().splitlines()))
        with open('Ws.txt') as f:
            self.vector_width = list(map(int, f.read().splitlines()))

    def change_current_image(self, image):
        self.image = image

    def set_scramble_modulo(self):
        self.modulo_row = self.generate_scramble_modulo(self.vector_height)
        self.modulo_column = self.generate_scramble_modulo(self.vector_width)

    @staticmethod
    def generate_scramble_modulo(vector):
        return ((vector[11]+vector[22]+vector[33])*vector[55]) % (len(vector) - 1)

    def column_scramble(self, scramble, column):
        elements_sum = 0
        for j in range(self.height):
            elements_sum += self.image[j][column]
        modulo_shift_column = elements_sum % self.modulo_column
        shift_direction = modulo_shift_column % 2
        if not scramble:
            shift_direction -= 1
        if shift_direction != 0:
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
        if shift_direction != 0:
            self.image[row, :] = np.roll(self.image[row, :], modulo_shift_row)
        else:
            self.image[row, :] = np.roll(self.image[row, :], -modulo_shift_row)

    def circular_scramble_alternate(self):
        number_of_iterations = self.generate_number_of_iterations() + 3
        for j in range(number_of_iterations):
            for i in range(self.width):
                self.row_scramble(True, i)
                self.column_scramble(True, i)

    def generate_number_of_iterations(self):
        return ((self.vector_height[7]+self.vector_height[77])*(self.vector_width[7]+self.vector_width[77])) % 4

    @staticmethod
    def xor_operation(source_list, vector_element):
        copy_to_return = source_list.copy()
        for i in range(len(copy_to_return)):
            copy_to_return[i] = copy_to_return[i] ^ vector_element
        return copy_to_return

    def rows_xor_operation(self):
        for row in range(self.height):
            rotated_height_vector = self.vector_height[::-1]
            option = row % 2
            if option != 0:
                self.image[row, :] = self.xor_operation(self.image[row], self.vector_height[row])
            else:
                self.image[row, :] = self.xor_operation(self.image[row], rotated_height_vector[row])

    def columns_xor_operation(self):
        for column in range(self.width):
            rotated_width_vector = self.vector_width[::-1]
            option = column % 2
            if option != 0:
                self.image[:, column] = self.xor_operation(self.image[:, column], self.vector_width[column])
            else:
                self.image[:, column] = self.xor_operation(self.image[:, column], rotated_width_vector[column])

    def xor_encryption(self):
        self.rows_xor_operation()
        self.columns_xor_operation()

    def xor_decryption(self):
        self.columns_xor_operation()
        self.rows_xor_operation()

##############################################################################################
    def row_scramble_standard(self, scramble):
        for row in range(self.height):
            elements_sum = 0
            for row_elements in range(self.width):
                elements_sum += self.image[row][row_elements]
            shift_length = elements_sum % 2
            if not scramble:
                shift_length -= 1

            if shift_length != 0:
                self.image[row, :] = np.roll(self.image[row, :], self.vector_height[row])
            else:
                self.image[row, :] = np.roll(self.image[row, :], -self.vector_height[row])
    def column_scramble_standard(self, scramble):
        for column in range(self.width):
            elements_sum = 0
            for j in range(self.height):
                elements_sum += self.image[j][column]

            shift_direction = elements_sum % 2
            if not scramble:
                shift_direction -= 1

            if shift_direction != 0:
                self.image[:, column] = np.roll(self.image[:, column], -self.vector_width[column])
            else:
                self.image[:, column] = np.roll(self.image[:, column], self.vector_width[column])

    def circular_scramble_standard(self):
        self.row_scramble_standard(True)
        self.column_scramble_standard(True)

    def un_scramble(self):
        self.column_scramble_standard(False)
        self.row_scramble_standard(False)
