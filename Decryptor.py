from Cryptography import Cryptography


class Decryptor(Cryptography):

    def __init__(self, path):
        super().__init__(path)
        self.load_generate_vectors()
        if len(self.main_image.shape) > 2:
            self.split_color_channels()
        self.remove_scramble_color_channels()

    def remove_scramble(self):
        self.xor_decryption()
        self.circular_un_scramble_alternate()

    def remove_scramble_color_channels(self):
        if len(self.main_image.shape) < 3:
            self.remove_scramble()
            return
        gray = self.check_if_gray_color(self.main_image)
        self.set_image_to_blue_channel()
        self.remove_scramble()
        if gray:
            self.main_image[:, :, 1] = self.main_image[:, :, 0]
            self.main_image[:, :, 2] = self.main_image[:, :, 0]
        else:
            self.set_image_to_green_channel()
            self.remove_scramble()
            self.set_image_to_red_channel()
            self.remove_scramble()

