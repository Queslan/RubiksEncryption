import ImageProcessing as iP
import cv2
import Cryptography as cG
import time


def encrypt_image(image):
    encryption.change_current_image(image)
    encryption.circular_scramble_alternate()
    #encryption.xor_encryption()


def encrypt_all_channels():
    encrypt_image(encryption.blue)
    encrypt_image(encryption.green)
    encrypt_image(encryption.red)


start_time = time.time()
image_og = iP.get_image("img/lena_gray.png")
encryption = cG.Cryptography(image_og)
encryption.split_color_channels()
encryption.generate_scrambling_vectors()
cv2.imshow("Before scramble", image_og)

encrypt_all_channels()


cv2.imwrite('scrambled.png', image_og)
cv2.imshow('After scramble', image_og)
elapsed_time = time.time() - start_time
print(elapsed_time)
cv2.waitKey(0)
