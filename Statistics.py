import cv2
import math
import numpy as np
from matplotlib import pyplot as plt

def histogram():
    img = cv2.imread('bpg_part.png')
    b, g, r = cv2.split(img)
    plt.hist(b.ravel(), 256, [0, 256]);
    plt.hist(g.ravel(), 256, [0, 256]);
    plt.hist(r.ravel(), 256, [0, 256]);
    plt.show()

def histogram2():
    img = cv2.imread('bpg_part.png', 0)
    plt.hist(img.ravel(), 256, [0, 256]);
    plt.show()
#histogram2()

#histogram()
def numbers_of_pixels_change_rate():
    image_original = cv2.imread('img/rgb16bit.ppm')
    image_encrypted = cv2.imread('scrambled.png')
    height = image_original.shape[0]
    width = image_original.shape[1]
    sum_of_all = 0
    for channel in range(3):
        one_channel_original = image_original[:, :, channel]
        one_channel_encrypted = image_encrypted[:, :, channel]
        sum_of_numbers = 0
        for h in range(height):
            for w in range(width):
                if one_channel_original[h][w] != one_channel_encrypted[h][w]:
                    sum_of_numbers += 1
        sum_of_all += sum_of_numbers

    average_sum = sum_of_all / 3
    result = average_sum / (height * width) * 100
    print(result)

numbers_of_pixels_change_rate()


def unified_average_changing_intensity():
    image_original = cv2.imread('img/rgb16bit.ppm')
    image_encrypted = cv2.imread('scrambled.png')
    height = image_original.shape[0]
    width = image_original.shape[1]
    sum_of_all = 0
    for channel in range(3):
        one_channel_original = image_original[:, :, channel]
        one_channel_encrypted = image_encrypted[:, :, channel]
        sum_of_numbers = 0
        for h in range(height):
            for w in range(width):
                difference = int(one_channel_original[h][w]) - int(one_channel_encrypted[h][w]) # with int cast
                sum_of_numbers += math.fabs(difference) / 255

        sum_of_all += sum_of_numbers
        print(sum_of_all)

    average_sum = sum_of_all / 3
    result = average_sum / (height * width) * 100
    print(result)

unified_average_changing_intensity()