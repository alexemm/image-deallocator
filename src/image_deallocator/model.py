from file_tools import save_json, load_json
from typing import List, Optional

# File for handling json "database""

DB_DIR = 'meta/data.json'
IMAGE_DIR = 'img/'


def create_db(direction):
    """

    :param direction:
    :return:
    """
    save_json(direction, {})


def add_original_image(name: str, filename: Optional[str] = None):
    """

    :param name:
    :param filename:
    :return:
    """
    name = name.lower()
    data = load_json(DB_DIR)
    if name not in data.keys():
        data[name] = []
    id = len(data[name])
    if filename is None:
        filename = '%s.png' % name
    direction = IMAGE_DIR + "%s/%i/%s" % (name, id, filename)
    new_obj = {
        'name': name,
        'dir': direction,
        'new_imgs': {}
    }
    data[name].append(new_obj)
    save_json(DB_DIR, data)
    return new_obj


def add_new_image(name: str, id: int, new_name, dirs: List[str]):
    """

    :param name:
    :param id:
    :param new_name:
    :param dirs:
    :return:
    """
    name = name.lower()
    data = load_json(DB_DIR)
    try:
        data[name][id]['new_imgs'][new_name] = {
            "new_name": new_name,
            "dirs": dirs
        }
    except KeyError as e:
        print(e)
        return
    save_json(DB_DIR, data)


def get_image(name: str, id: int):
    name = name.lower()
    data = load_json(DB_DIR)
    if name not in data.keys():
        return None
    if id not in range(0, len(data[name])):
        return None
    return data[name][id]


def delete_original_image(name: str, id: int):
    """

    :param name:
    :param id:
    :return:
    """
    name = name.lower()
    data = load_json(DB_DIR)
    if name not in data.keys():
        return
    if id not in range(0, len(data[name])):
        return
    data[name].pop(id)
    if len(data[name]) == 0:
        data.pop(name)
    save_json(DB_DIR, data)


def drop_db(direction):
    """

    :param direction:
    :return:
    """
    save_json(direction, None)


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
