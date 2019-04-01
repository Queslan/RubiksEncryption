import cv2
from Cryptography import Cryptography


class Encryptor(Cryptography):

    def __init__(self, path):
        super().__init__(path)
        if len(self.image.shape) > 2:
            self.split_color_channels()
        self.generate_scrambling_vectors()
        self.encrypt_all_channels()
        self.encryption_path = "result/encrypted.png"

    def encrypt_image(self):
        self.circular_scramble_alternate()
        self.xor_encryption()

    def encrypt_all_channels(self):
        if len(self.image.shape) < 3:
            self.encrypt_image()
            return
        gray = Encryptor.check_if_gray_color(self.image)
        self.set_image_to_blue_channel()
        self.encrypt_image()
        if gray:
            self.main_image[:, :, 1] = self.main_image[:, :, 0]
            self.main_image[:, :, 2] = self.main_image[:, :, 0]
        else:
            self.set_image_to_green_channel()
            self.encrypt_image()
            self.set_image_to_red_channel()
            self.encrypt_image()

    def save_file(self):
        cv2.imwrite(self.encryption_path, self.main_image)

    def show_encrypted(self):
        cv2.imshow('After scramble', self.main_image)
        cv2.waitKey(0)


