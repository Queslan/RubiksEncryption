import cv2
import math
import numpy as np
from matplotlib import pyplot as plt
import random


def histogram(image_content):
    if len(image_content.shape) < 3 :
        plt.hist(image_content.ravel(), 256, [0, 256], color='black')
    else:
        b, g, r = cv2.split(image_content)
        if np.array_equal(b, g) and np.array_equal(g, r):
            plt.hist(b.ravel(), 256, [0, 256], color='black')
        else:
            plt.hist(b.ravel(), 256, [0, 256], color='blue')
            plt.hist(g.ravel(), 256, [0, 256], color='green')
            plt.hist(r.ravel(), 256, [0, 256], color='red')
    plt.savefig("result/histogram.png")
    #plt.show()
    plt.close()


def numbers_of_pixels_change_rate(image_original, image_encrypted):
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


def unified_average_changing_intensity(image_original, image_encrypted):
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


list_of_test_images = ['baboon_color.png', 'baboon_gray.png', 'black.png', 'lena_color.png', 'lena_gray.png']


def make_histograms_for_list(images_list):
    for image_name in images_list:
        histogram(cv2.imread('img/' + image_name))
        image_name = 'encrypted_' + image_name
        histogram(cv2.imread('encrypted/' + image_name))

        #with open("visual_changes.txt", "a") as text_file:
         #   text_file.write(image_name + ' - NPCR: ' + '%.2f' % numbers_of_pixels_change_rate() +
          #                  " UACI: " + '%.2f' % unified_average_changing_intensity() + '\n')


def salt_and_pepper(image,prob):
    output = np.zeros(image.shape,np.uint8)
    thres = 1 - prob
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            rdn = random.random()
            if rdn < prob:
                output[i][j] = 0
            elif rdn > thres:
                output[i][j] = 255
            else:
                output[i][j] = image[i][j]
    return output


#img = cv2.imread('encrypted/encrypted.png')
#attacked = salt_and_pepper(img, 0.05)
#cv2.imwrite('attacked.png', attacked)
#cv2.imshow('attacked', attacked)
#cv2.waitKey(0)