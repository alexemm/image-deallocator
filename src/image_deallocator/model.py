from werkzeug.datastructures import FileStorage

from file_tools import save_json, load_json
from typing import List, Optional, Dict

# File for handling json "database"

DB_DIR: str = 'meta/data.json'
IMAGE_DIR: str = 'img/'


def create_db(directory: str) -> None:
    """
    Creates empty json object representing a database
    :param directory: Directory of json file
    :return: None
    """
    save_json(directory, {})


def add_original_image(name: str, filename: Optional[str] = None) -> Dict[str, any]:
    """
    Adds new original image in meta file with additional directories and returns created object.
    :param name: Name of image
    :param filename: Filename
    :return: Created new object
    """
    name: str = name.lower()
    data: Dict[str, any] = load_json(DB_DIR)
    if name not in data.keys():
        data[name]: List[Dict[str, any]] = []
    id: int = len(data[name])
    filename: str = name + '.' + filename.split('.')[-1]
    directory: str = IMAGE_DIR + "%i-%s" % (id, filename)
    new_obj: Dict[str, any] = {
        'name': name,
        'dir': directory,
        'new_imgs': {}
    }
    data[name].append(new_obj)
    save_json(DB_DIR, data)
    return new_obj


def add_new_image(name: str, id: int, new_name, dirs: List[str], axis: int = 0) -> None:
    """
    Adds new image with all the directories for given original image in meta
    :param name: Name of image
    :param id: Id of image
    :param new_name:  New  name of which image should be generated
    :param dirs: List of directories to the new images
    :param axis: 0 for horizontal and 1 for vertical
    :return: None
    """
    name: str = name.lower()
    data: Dict[str, any] = load_json(DB_DIR)
    if name not in data.keys():
        return
    if id not in range(0, len(data[name])):
        return
    if new_name not in data[name][id]['new_imgs'].keys():
        data[name][id]['new_imgs'][new_name]: Dict[str, any] = {
            "new_name": new_name,
            "dirs": {"axis": [[], []]}
        }
    data[name][id]['new_imgs'][new_name]['dirs']['axis'][axis]: List[str] = dirs
    save_json(DB_DIR, data)


def get_image(name: str, id: int) -> Dict[str, any]:
    """
    Returns the image object from meta based on given name and id
    :param name: Name of image
    :param id: Id of image
    :return: Image object with name, directory, and new images (if there are any)
    """
    name: str = name.lower()
    data: Dict[str, any] = load_json(DB_DIR)
    if name not in data.keys():
        return None
    if id not in range(0, len(data[name])):
        return None
    return data[name][id]


def delete_original_image(name: str, id: int) -> None:
    """
    Deletes an original image in meta based on given name and id. Does nothing, if image does not exist.
    :param name: Name of image
    :param id: Id of image
    :return: None
    """
    name: str = name.lower()
    data: Dict[str, any] = load_json(DB_DIR)
    if name not in data.keys():
        return
    if id not in range(0, len(data[name])):
        return
    data[name].pop(id)
    if len(data[name]) == 0:
        data.pop(name)
    save_json(DB_DIR, data)


def drop_db(directory: str) -> None:
    """
    Drops whole meta and leaves it empty. Database needs to be created again.
    :param directory: Directory of db
    :return: None
    """
    save_json(directory, None)


test_cases = [None,
              {},
              {"test": [{"name": "test", "dir": "img/test/0/test.png", "new_imgs": {}}]},
              {"test": [{"name": "test", "dir": "img/test/0/test.png", "new_imgs": {}}],
               "test2": [{"name": "test2", "dir": "img/test2/0/test2.png", "new_imgs": {}}]},
              {"test": [{"name": "test", "dir": "img/test/0/test.png", "new_imgs": {}},
                        {"name": "test", "dir": "img/test/1/test.png", "new_imgs": {}}],
               "test2": [{"name": "test2", "dir": "img/test2/0/test2.png", "new_imgs": {}}]},
              {"test": [{"name": "test", "dir": "img/test/1/test.png", "new_imgs": {}}],
               "test2": [{"name": "test2", "dir": "img/test2/0/test2.png", "new_imgs": {}}]},
              {"test2": [{"name": "test2", "dir": "img/test2/0/test2.png", "new_imgs": {}}]},
              {"test2": [{"name": "test2", "dir": "img/test2/0/test2.png",
                          "new_imgs": {"ee": {"new_name": "ee", "dirs": ["new_img"]}}}]},
              ]


def test_equals(direction, id):
    assert load_json(direction) == test_cases[id]


def test():
    global DB_DIR
    DB_DIR = "meta/test.json"
    print("Drop DB")
    drop_db(DB_DIR)
    test_equals(DB_DIR, 0)
    print("DB completely empty")
    print("Create DB")
    create_db(DB_DIR)
    test_equals(DB_DIR, 1)
    print("DB creation successful")
    print("Add 2 original images")
    add_original_image("test")
    test_equals(DB_DIR, 2)
    add_original_image("test2")
    test_equals(DB_DIR, 3)
    add_original_image("test")
    test_equals(DB_DIR, 4)
    print("Added images successfully")
    print("Delete test")
    delete_original_image("test", 0)
    test_equals(DB_DIR, 5)
    delete_original_image("test", 0)
    test_equals(DB_DIR, 6)
    print("Delete test")
    print("Add new image")
    add_new_image("test2", 0, "ee", ["new_img"])
    test_equals(DB_DIR, 7)
    print("Added new image successfully")


if __name__ == '__main__':
    test()
