import cv2
import math
import numpy as np
from matplotlib import pyplot as plt
image_name = 'baboon_gray'
image_format = '.png'
image_original = cv2.imread('img/'+image_name+image_format)
image_encrypted = cv2.imread('encrypted/'+image_name+'_encrypted'+image_format)


def histogram():
    b, g, r = cv2.split(image_original)
    plt.hist(b.ravel(), 256, [0, 256]);
    plt.hist(g.ravel(), 256, [0, 256]);
    plt.hist(r.ravel(), 256, [0, 256]);
    plt.show()


def histogram2():
    plt.hist(image_original.ravel(), 256, [0, 256]);
    plt.show()


def numbers_of_pixels_change_rate():
    height = image_original.shape[0]
    width = image_original.shape[1]
    sum_of_all = 0
    if len(image_original.shape) < 3:
        sum_of_numbers = 0
        for h in range(height):
            for w in range(width):
                if image_original[h][w] != image_encrypted[h][w]:
                    sum_of_numbers += 1
            sum_of_all += sum_of_numbers
        result = sum_of_all / (height * width) * 100
        return result
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
    return result


def unified_average_changing_intensity():
    height = image_original.shape[0]
    width = image_original.shape[1]
    sum_of_all = 0
    if len(image_original.shape) < 3:
        sum_of_numbers = 0
        for h in range(height):
            for w in range(width):
                if image_original[h][w] != image_encrypted[h][w]:
                    difference = int(image_original[h][w]) - int(image_encrypted[h][w])  # with int cast
                    sum_of_numbers += math.fabs(difference) / 255
        sum_of_all += sum_of_numbers
        result = sum_of_all / (height * width) * 100
        return result
    for channel in range(3):
        one_channel_original = image_original[:, :, channel]
        one_channel_encrypted = image_encrypted[:, :, channel]
        sum_of_numbers = 0
        for h in range(height):
            for w in range(width):
                difference = int(one_channel_original[h][w]) - int(one_channel_encrypted[h][w]) # with int cast
                sum_of_numbers += math.fabs(difference) / 255

        sum_of_all += sum_of_numbers
    average_sum = sum_of_all / 3
    result = average_sum / (height * width) * 100
    return result


with open("visual_changes.txt", "a") as text_file:
    text_file.write(image_name+image_format + ' - NPCR: ' + '%.2f' % numbers_of_pixels_change_rate() +
                    " UACI: " + '%.2f' % unified_average_changing_intensity() + '\n')
print(numbers_of_pixels_change_rate())
print(unified_average_changing_intensity())
