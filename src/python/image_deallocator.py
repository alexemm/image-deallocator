import cv2 as cv
import json
import numpy as np
import itertools as it

from collections import defaultdict
from typing import List, Dict
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


def get_divisions(img: np.ndarray, name: str, axis: int = 0) -> Dict[str, List[np.ndarray]]:
    """
    Divides the image, based on the character which is allocated to. This handles also the special case, where not all
    chars in the string are unique.
    :param img: Image representation as a numpy array
    :param name: Name
    :param axis: 0 for horizontal and 1 for vertical
    :return: Divisions based on position of char. Returned as List of dictionaries
    """
    # TODO: Implement this
    ret = defaultdict(list)
    for key, value in zip(list(name), np.array_split(img, len(name), axis=axis)):
        ret[key].append(value)
    return dict(ret)


def assemble_img(new_name: str, locator: Dict[str, List[np.ndarray]], axis: int = 0) -> List[np.ndarray]:
    """
    Assembles parts of the old image to a new image based on the new name.
    :param new_name: New name, which only consists of characters from the original name
    :param locator: Dictionary of the divided parts into the posiitional characters
    :param axis: 0 for horizontal and 1 for vertical
    :return: New image representation as a numpy array
    """
    new_name = new_name.lower()
    if not set(new_name) <= set(locator.keys()):
        new_name = ''.join(locator.keys()).lower()
    indices = [i for i in it.product(*[list(range(0, len(locator[c]))) for c in new_name])]
    return [np.concatenate([locator[c][index[idx]] for idx, c in enumerate(new_name)], axis=axis) for index in indices]


def deallocate_img(data: Dict[str, str], new_name: str, axis: int = 0) -> List[np.ndarray]:
    """
    Divides image into parts based on given name and assembles it to a new image based on new name
    :param data: Object consisting of name and direction
    :param new_name: Name
    :param axis: 0 for horizontal and 1 for vertical
    :return: New image representation as a numpy array
    """
    name, direction = data['name'], data['dir']
    img = load_img(direction)
    divisions = get_divisions(img, name, axis)
    return assemble_img(new_name, divisions, axis)


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


def test_image_deallocation():
    file = 'meta/data.json'
    data = load_json(file)[0]
    print(data)
    new_name = 'toto'
    imgs = deallocate_img(data, new_name, 0)
    # for img in imgs:
    #     cv.imshow("EEEEE", img)
    #     cv.waitKey(0)
    save_images(new_name, imgs)


if __name__ == "__main__":
    test_image_deallocation()
