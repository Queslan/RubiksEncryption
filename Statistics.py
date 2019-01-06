import cv2
import math
import numpy as np
from matplotlib import pyplot as plt

def histogram():
    img = cv2.imread('rubik_colors.png')
    color = ('b','g','r')
    for i,col in enumerate(color):
        histr = cv2.calcHist([img],[i],None,[256],[0,256])
        plt.plot(histr,color = col)
        plt.xlim([0,256])
    plt.show()


def numbers_of_pixels_change_rate():
    image_original = cv2.imread('gray8bit.png')
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
    image_original = cv2.imread('gray8bit.png')
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
                #difference = one_channel_original[h][w] - one_channel_encrypted[h][w]
                sum_of_numbers += math.fabs(difference) / 255

        sum_of_all += sum_of_numbers
        print(sum_of_all)

    average_sum = sum_of_all / 3
    result = average_sum / (height * width) * 100
    print(result)

unified_average_changing_intensity()