from typing import List, Dict

import json
import cv2 as cv
import numpy as np
from os import path, makedirs


def load_json(file: str) -> Dict[str, str]:
    """
    Loads json file as a dictionary
    :param file: relative path to file
    :return: Dictionary of given file
    """
    with open(file) as f:
        data = json.load(f)
    return data


def save_json(file: str, dic) -> None:
    """

    :param file:
    :param dic:
    :return:
    """
    with open(file, 'w+') as f:
        json.dump(dic, f)


def load_img(file: str) -> np.ndarray:
    """
    Loads image file as 3D-Matrix
    :param file: relative path to file
    :return: image file as Numpy 3D-Matrix
    """
    return cv.imread(file, cv.IMREAD_UNCHANGED)


def save_img(name: str, img: np.ndarray) -> None:
    """
    Saves numpy array as image file
    :param name: Name of file
    :param img: Image representation as a numpy array
    :param dir: directory to destination folder
    :return: None
    """
    cv.imwrite(name, img)


def save_images(images: List[np.ndarray], directory: str = 'new_img/') -> List[str]:
    """
    Creates folder if there is none and saves all the images in the list
    :param name: Name of person in image
    :param images: List of images
    :param directory: directory to destination folder
    :return:
    """
    if not path.exists(directory):
        makedirs(directory)
    filenames = []
    for i, img in enumerate(images):
        filename = "%s%i.png" % (directory, i)
        save_img(filename, img)
        filenames.append(filename)
    return filenames
