from typing import List, Dict

import json
import cv2 as cv
import numpy as np
from os import path, mkdir


def load_json(file: str) -> Dict[str, str]:
    """
    Loads json file as a dictionary
    :param file: relative path to file
    :return: Dictionary of given file
    """
    with open(file) as file:
        data = json.load(file)
    return data


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


def save_images(name: str, images: List[np.ndarray], dir: str = 'new_img/') -> None:
    """
    Creates folder if there is none and saves all the images in the list
    :param name: Name of person in image
    :param images: List of images
    :param dir: directory to destination folder
    :return:
    """
    dest = dir + name
    if not path.exists(dest):
        mkdir(dest)
    for i, img in enumerate(images):
        save_img("%s/%i.png" % (dest, i), img)
