import ImageProcessing as iP
import cv2
import Cryptography as cG
import time


def encrypt_image(image):
    encryption.change_current_image(image)
    encryption.rows_circular_shift(True)
    encryption.columns_circular_shift(True)
    encryption.rows_xor_operation()
    encryption.columns_xor_operation()


def encrypt_all_channels():
    encrypt_image(encryption.blue)
    encrypt_image(encryption.green)
    encrypt_image(encryption.red)


start_time = time.time()
image_og = iP.get_image("bpg_part.png")
encryption = cG.Cryptography(image_og)
encryption.split_color_channels()
encryption.generate_scrambling_vectors(8)
cv2.imshow("Before scramble", image_og)

encrypt_all_channels()


cv2.imwrite('scrambled.png', image_og)
cv2.imshow('After scramble', image_og)
elapsed_time = time.time() - start_time
print(elapsed_time)
cv2.waitKey(0)
