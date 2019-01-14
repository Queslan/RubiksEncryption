import cv2
import ImageProcessing as iP
import Cryptography as cG
import time


def remove_scramble():
    decryption.xor_decryption()
    decryption.circular_un_scramble_alternate()


def remove_scramble_color_channels():
    if len(main_image.shape) < 3:
        remove_scramble()
        return
    gray = cG.Cryptography.check_if_gray_color(main_image)
    decryption.set_image_to_blue_channel()
    remove_scramble()
    if gray:
        main_image[:, :, 1] = main_image[:, :, 0]
        main_image[:, :, 2] = main_image[:, :, 0]
    else:
        decryption.set_image_to_green_channel()
        remove_scramble()
        decryption.set_image_to_red_channel()
        remove_scramble()


main_image = iP.get_image('encrypted/baboon_gray_encrypted.png')
start_time = time.time()
decryption = cG.Cryptography(main_image)
decryption.load_generate_vectors()
if len(main_image.shape) > 2:
    decryption.split_color_channels()
cv2.imshow("Scrambled image", main_image)
remove_scramble_color_channels()
iP.show_image("Scramble removed", main_image)
elapsed_time = time.time() - start_time
print(elapsed_time)

cv2.waitKey(0)
