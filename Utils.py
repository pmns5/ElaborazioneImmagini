from enum import Enum

import cv2
import matplotlib.pyplot as plt
import numpy as np
import skimage as sk
from skimage.metrics import mean_squared_error as mse
from skimage.metrics import structural_similarity as ssim


def im2double(im):
    min_val = np.min(im.ravel())
    max_val = np.max(im.ravel())
    out = (im.astype('float') - min_val) / (max_val - min_val)
    return out


def show_image(image, title):
    """ Display image through pyplot """
    plt.figure()
    plt.imshow(image, cmap='gray')
    plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
    plt.title(title)


def evaluate(imageA, imageB, rgb_flag):
    imageA = im2double(imageA)
    imageB = im2double(imageB)
    m = mse(imageA, imageB)
    p = cv2.PSNR(imageA, imageB)
    s = ssim(imageA, imageB, multichannel=rgb_flag)
    return m, p, s


def add_noise(image, noise_type, sigma_g=0.1, mean_g=0, p_sp=0.05):
    """ Add the specified noise to the image """
    noisy = None

    if noise_type.value == "gaussian":  # Gaussian Noise
        ifl = sk.util.img_as_float(image.copy())
        noise_g = mean_g + sigma_g * np.random.randn(*image.shape)
        noisy = np.clip(ifl + noise_g, 0.0, 1.0)
    elif noise_type.value == "s&p":  # Salt and Pepper noise
        noisy = sk.util.img_as_float(image.copy())
        noisy[np.random.rand(*noisy.shape) < p_sp / 2] = 0
        aux = np.random.rand(*noisy.shape)
        noisy[(aux > p_sp / 2) & (aux < p_sp)] = 1
    elif noise_type.value == "poisson":  # Poisson noise
        noisy = sk.util.random_noise(image, 'poisson')
    elif noise_type.value == "speckle":  # Speckle noise
        noisy = sk.util.random_noise(image, 'speckle')
    return noisy


def get_channels_number(image):
    """ Return the number of channels of the image """
    return 1 if len(image.shape) == 2 else image.shape[2]


def bgr2rgb(image):
    image = im2double(image)
    return image[:, :, 2::-1]


class Noise(Enum):
    GAUSSIAN = "gaussian"
    SALT_AND_PEPPER = "s&p"
    POISSON = "poisson"
    SPECKLE = "speckle"
