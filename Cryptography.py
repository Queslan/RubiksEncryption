from collections import deque
from random import randint


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

    def list_180_rotation(self, source_list):
        list_to_deque = deque(source_list)
        list_size = len(source_list)
        list_to_deque.rotate(list_size)
        return list(list_to_deque)


    def xor_operation(self, source_list, vector_element):
        copy_to_return = source_list.copy()
        for element in copy_to_return:
             element = element ^ vector_element
        return copy_to_return


    def put_column(self, shifted, column_number, image):
        for j in range(self.height):
            image[j][column_number] = shifted[j]


    def whole_column(self, matrix, i):
        return [row[i] for row in matrix]

    def circular_shift(self, shift_length, source_list):  # deque.rotate(n) for n > 0 - right, n < 0 - left
        list_to_deque = deque(source_list)
        list_to_deque.rotate(shift_length)
        return list(list_to_deque)

    def split_color_channels(self):  # B G R
        self.blue = self.image[:, :, 0]
        self.green = self.image[:, :, 1]
        self.red = self.image[:, :, 2]

    def generate_scrambling_vectors(self, image_bit_size):
        biggest_element = pow(2, image_bit_size)-1
        for i in range(self.height):
            self.height_vector.append(randint(0, biggest_element))
        for j in range(self.width):
            self.width_vector.append(randint(0, biggest_element))

        with open("KeyH.txt", "w") as text_file:
            text_file.write('\n'.join(str(element) for element in self.height_vector))
        with open("KeyW.txt", "w") as text_file:
            text_file.write('\n'.join(str(element) for element in self.width_vector))

    def load_generate_vectors(self):
        with open('KeyH.txt') as f:
            self.height_vector = list(map(int, f.read().splitlines()))
        with open('KeyW.txt') as f:
            self.width_vector = list(map(int, f.read().splitlines()))


    def rows_circular_shift(self,scrambling):
        for row in range(self.height):
            elements_sum = 0
            for row_elements in range(self.width):
                elements_sum += self.image[row][row_elements]

            shift_length = elements_sum % 2
            if not scrambling:
                shift_length -= 1

            if shift_length != 0:
                self.image[row] = self.circular_shift(self.height_vector[row], self.image[row])
            else:
                self.image[row] = self.circular_shift(-self.height_vector[row], self.image[row])


    def columns_circular_shift(self, scrambling):
        for i in range(self.width):
            elements_sum = 0
            for j in range(self.height):
                elements_sum += self.image[j][i]

            shift_direction = elements_sum % 2
            if not scrambling:
                shift_direction -= 1

            if shift_direction != 0:
                shift = self.circular_shift(self.width_vector[i], self.whole_column(self.image, i))
            else:
                shift = self.circular_shift(-self.width_vector[i], self.whole_column(self.image, i))
            self.put_column(shift, i, self.image)


    def rows_xor_operation(self):
        rotated_height_vector = self.list_180_rotation(self.height_vector)
        for row in range(self.height):
            option = row % 2
            if option != 0:
                self.image[row] = self.xor_operation(self.image[row], self.height_vector[row])
            else:
                self.image[row] = self.xor_operation(self.image[row], rotated_height_vector[row])


    def columns_xor_operation(self):
        rotated_width_vector = self.list_180_rotation(self.width_vector)
        for column in range(self.width):
            option = column % 2
            if option != 0:
                shift = self.xor_operation(self.whole_column(self.image, column), self.width_vector[column])
            else:
                shift = self.xor_operation(self.whole_column(self.image, column), rotated_width_vector[column])
            self.put_column(shift, column, self.image)

    def change_current_image(self, image):
        self.image = image

