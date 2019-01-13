import cv2
import ImageProcessing as iP
import Cryptography as cG
import time


def remove_scramble(scrambled_image):
    decryption.change_current_image(scrambled_image)
    decryption.xor_decryption()
    decryption.circular_un_scramble_alternate()


def remove_scramble_color_channels():
    remove_scramble(decryption.blue)
    remove_scramble(decryption.green)
    remove_scramble(decryption.red)


start_time = time.time()
image_og = iP.get_image('scrambled.png')
decryption = cG.Cryptography(image_og)
decryption.load_generate_vectors()
decryption.split_color_channels()
cv2.imshow("Scrambled image", image_og)
remove_scramble_color_channels()
iP.show_image("Scramble removed", image_og)
elapsed_time = time.time() - start_time
print(elapsed_time)

cv2.waitKey(0)
