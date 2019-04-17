import cv2
import math
import numpy as np
from matplotlib import pyplot as plt
import random
import skimage
from Cryptography import Cryptography
from sklearn.metrics import mean_squared_error

original_paths = ["img\lena_color.png",
        "img\lena_gray.png",
        "img\\black.png",
        "img\\baboon_color.png",
        "img\\baboon_gray.png"]

encrypted_paths = ["encrypted_lib\lena_color_encrypted.png",
                   "encrypted_lib\lena_gray_encrypted.png",
                   "encrypted_lib\\black_encrypted.png",
                   "encrypted_lib\\baboon_color_encrypted.png",
                   "encrypted_lib\\baboon_gray_encrypted.png"]



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

        for h in range(height):
            sum_of_numbers = 0
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

        for h in range(height):
            sum_of_numbers = 0
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


def count_entropy():
    for path in original_paths:
        img = cv2.imread(path)
        entropy = skimage.measure.shannon_entropy(img)
        print(entropy)

    print("---------------------------------------------------------------")

    for path in encrypted_paths:
        img = cv2.imread(path)
        entropy = skimage.measure.shannon_entropy(img)
        print(entropy)


def count_mse(imageA, imageB):
    # the 'Mean Squared Error' between the two images is the
    # sum of the squared difference between the two images;
    # NOTE: the two images must have the same dimension
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])

    # return the MSE, the lower the error, the more "similar"
    # the two images are
    return err

def attack_operations():
    img = cv2.imread('result/encrypted.png')
    attacked = salt_and_pepper(img, 0.05)
    cv2.imwrite('attacked.png', attacked)
    attacked_encrypted = cv2.imread('result/decrypted.png')
    original_img = cv2.imread("img/black.png")
    second_mse = count_mse(original_img, attacked_encrypted)
    print(second_mse)

def rows_correlation(image, N):
    sum = 0
    for i in range(N):
        if i+1 < image.shape[0]:
            x = image[i, :, 1], image[i+1, :, 1]
            cor_coef = np.corrcoef(x)
            sum += cor_coef
    return sum / N

def columns_correlation(image, N):
    sum = 0
    for i in range(N):
        if i + 1 < image.shape[0]:
            x = image[:, i, 1], image[:, i + 1, 1]
            cor_coef = np.corrcoef(x)
            sum += cor_coef
    return sum / N

def diagonal_correlation(image, N):
    sum = 0
    for i in range(N):
        if i + 1 < image.shape[0]:
            ##I need array
            x = make_diagonal(image[:, :, 1], i+10)
            cor_coef = np.corrcoef(x)
            sum += cor_coef
    return sum / N

def make_diagonal(image, iterator):
    diagonal_of_image = []
    for i in range(iterator + 1):
        diagonal_of_image.append(image[i][i])

    return np.array(diagonal_of_image)


def get_all_corelations(image, N):
    print("rows correlation: ")
    print(rows_correlation(image, N))
    print("columns corelation: ")
    print(columns_correlation(image, N))
    print("diagonal_correlation: ")
    print(diagonal_correlation(image, N))

image = cv2.imread("img/baboon_gray.png")
get_all_corelations(image, 50)

######## From scratch file #############


def numbers_of_pixels_change_rate(image_original, image_encrypted):
    height = image_original.shape[0]
    width = image_original.shape[1]
    sum_of_all = 0
    if len(image_original.shape) < 3:
        for h in range(height):
            sum_of_numbers = 0
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


class Encryptor(Cryptography):

    def __init__(self, path, first_vector, second_vector):
        super().__init__(path)
        self.first_vector = first_vector
        self.second_vector = second_vector
        if len(self.image.shape) > 2:
            self.split_color_channels()

        if first_vector == None and second_vector == None :
            print("generate")
            self.generate_scrambling_vectors()
        else:
            print("load")
            self.load_generate_vectors()
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

    def save_file(self, name):
        cv2.imwrite("result/"+name+".png", self.main_image)

    def show_encrypted(self):
        cv2.imshow('After scramble', self.main_image)
        cv2.waitKey(0)

    def load_generate_vectors(self):
        with open(self.first_vector) as f:
            self.vector_height = list(map(int, f.read().splitlines()))
        with open(self.second_vector) as f:
            self.vector_width = list(map(int, f.read().splitlines()))
        self.set_scramble_modulo()

class Decryptor(Cryptography):

    def __init__(self, path, first_vector, second_vector):
        super().__init__(path)
        self.first_vector = first_vector
        self.second_vector = second_vector
        self.load_generate_vectors()
        if len(self.main_image.shape) > 2:
            self.split_color_channels()
        self.remove_scramble_color_channels()
        self.decryption_path = "result/decrypted.png"

    def remove_scramble(self):
        self.xor_decryption()
        self.circular_un_scramble_alternate()

    def remove_scramble_color_channels(self):
        if len(self.main_image.shape) < 3:
            self.remove_scramble()
            return
        gray = self.check_if_gray_color(self.main_image)
        self.set_image_to_blue_channel()
        self.remove_scramble()
        if gray:
            self.main_image[:, :, 1] = self.main_image[:, :, 0]
            self.main_image[:, :, 2] = self.main_image[:, :, 0]
        else:
            self.set_image_to_green_channel()
            self.remove_scramble()
            self.set_image_to_red_channel()
            self.remove_scramble()

    def load_generate_vectors(self):
        with open(self.first_vector) as f:
            self.vector_height = list(map(int, f.read().splitlines()))
        with open(self.second_vector) as f:
            self.vector_width = list(map(int, f.read().splitlines()))
        self.set_scramble_modulo()

    def save_file(self, name):
        cv2.imwrite("result/" + name + ".png", self.main_image)

def encryption_function():
    encryption = Encryptor("D:\\GitRepos\\RubiksEncryption\\img\\black.png", "Ww.txt", "Ws.txt")
    encryption.save_file("encrypted_origin")

    create_vector_with_different_last_bit()

    new_encryptor = Encryptor("D:\\GitRepos\\RubiksEncryption\\img\\black.png", "Ww2.txt", "Ws2.txt")
    new_encryptor.save_file("encrypted_changed_bit")

def decryption_function():
    decryption = Decryptor("D:\GitRepos\RubiksEncryption\\result\encrypted.png", "Ww.txt", "Ws.txt")
    decryption.save_file("decrypted_origin")

    create_vector_with_different_last_bit()

    new_decryption = Decryptor("D:\GitRepos\RubiksEncryption\\result\encrypted.png", "Ww2.txt", "Ws2.txt")
    new_decryption.save_file("decrypted_changed_bit")

def create_vector_with_different_last_bit():

    with open('Ww.txt') as f:
        vector_height = list(map(int, f.read().splitlines()))
    with open('Ws.txt') as f:
        vector_width = list(map(int, f.read().splitlines()))

    for i in range(512):
        if vector_height[i] & 1:
            vector_height[i] = vector_height[i]  & ~1
        else:
            vector_height[i] = vector_height[i] | 1

        if vector_width[i] & 1:
            vector_width[i] = vector_width[i] & ~1
        else:
            vector_width[i] = vector_width[i] | 1

    with open("Ww2.txt", "w") as text_file:
        text_file.write('\n'.join(str(element) for element in vector_height.copy()))
    with open("Ws2.txt", "w") as text_file:
        text_file.write('\n'.join(str(element) for element in vector_width.copy()))

#decryption_function()
#print(numbers_of_pixels_change_rate(ip.get_image("result/decrypted_origin.png"),
                                    #ip.get_image("result/decrypted_changed_bit.png")))


