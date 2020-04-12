import cv2 as cv
import json
import numpy as np

from collections import Counter
from typing import Dict, List


def load_json(file: str) -> Dict[str, str]:
    """
    Loads json file as a dictionary
    :param file: relative path to file
    :return: Dictionary of given file
    """
    with open(file) as file:
        data = json.load(file)
    return data


def load_img(file: str, mode: int = 1) -> np.ndarray:
    """
    Loads image file as 3D-Matrix
    :param file: relative path to file
    :param mode: 0 for grayscale, 1 for coloured
    :return: image file as Numpy 3D-Matrix
    """
    return cv.imread(file, mode)


def get_divisions(img: np.ndarray, name: str, axis: int = 0) -> Dict[str, np.ndarray]:
    """
    Divides the image, based on the character which is allocated to
    :param img: Image representation as a numpy array
    :param name: Name
    :param axis: 0 for horizontal and 1 for vertical
    :return: Divisions based on position of char. Returned as dictionary
    """
    name = name.lower()
    # Don't know how to handle multiple occurrence for one character
    if len(list(filter(lambda x: x[1] > 1, Counter(name).items()))) != 0:
        return get_divisions_non_determined(img, name, axis)[0]
    return dict(zip(list(name), np.array_split(img, len(name), axis=axis)))


def get_divisions_non_determined(img: np.ndarray, name: str, axis: int = 0) -> List[Dict[str, np.ndarray]]:
    """
    Divides the image, based on the character which is allocated to. This handles the special case, where not all chars
    in the string are unique.
    :param img: Image representation as a numpy array
    :param name: Name
    :param axis: 0 for horizontal and 1 for vertical
    :return: Divisions based on position of char. Returned as List of dictionaries
    """
    # TODO: Implement this
    return [{'': img}]


def assemble_img(new_name: str, locator: Dict[str, np.ndarray], axis: int = 0) -> np.ndarray:
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
    return np.concatenate([locator[c] for c in new_name], axis=axis)


def deallocate_img(data: Dict[str, str], new_name: str) -> np.ndarray:
    """
    Divides image into parts based on given name and assembles it to a new image based on new name
    :param data: Object consisting of name and direction
    :param new_name: Name
    :return: New image representation as a numpy array
    """
    name, direction = data['name'], data['dir']
    img = load_img(direction)
    divisions = get_divisions(img, name, 0)
    return assemble_img(new_name, divisions)


def save_img(name: str, img: np.ndarray) -> None:
    """
    Saves numpy array as image file
    :param name: Name of file
    :param img: Image representation as a numpy array
    :return: None
    """
    cv.imwrite(name, img)


def test_image_deallocation():
    file = 'meta/data.json'
    data = load_json(file)[0]
    print(data)
    new_name = 'toph'
    img = deallocate_img(data, new_name)
    cv.imshow("EEEEE", img)
    cv.waitKey(0)
    save_img('new_img/%s.png' % new_name, img)


if __name__ == "__main__":
    test_image_deallocation()
