import ImageProcessing as iP
import cv2
import Cryptography as cG
import time
import numpy as np


def encrypt_image():
    encryption.circular_scramble_alternate()
    encryption.xor_encryption()


def encrypt_all_channels():
    if len(main_image.shape) < 3:
        encrypt_image()
        return
    gray = cG.Cryptography.check_if_gray_color(main_image)
    encryption.set_image_to_blue_channel()
    encrypt_image()
    if gray:
        main_image[:, :, 1] = main_image[:, :, 0]
        main_image[:, :, 2] = main_image[:, :, 0]
    else:
        encryption.set_image_to_green_channel()
        encrypt_image()
        encryption.set_image_to_red_channel()
        encrypt_image()


image_name = 'baboon_gray'
image_format = '.png'
main_image = iP.get_image('img/' + image_name + image_format)
start_time = time.time()
encryption = cG.Cryptography(main_image)
if len(main_image.shape) > 2:
    encryption.split_color_channels()
encryption.generate_scrambling_vectors()
encrypt_all_channels()
elapsed_time = time.time() - start_time
with open("encryption_times.txt", "a") as text_file:
    text_file.write(image_name+image_format + ' : ' + '%.2f' % elapsed_time + '\n')
cv2.imwrite('encrypted/' + image_name +'_encrypted' + image_format, main_image)
cv2.imshow('After scramble', main_image)

cv2.waitKey(0)
