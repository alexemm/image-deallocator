from model import add_original_image, get_image, add_new_image
from image_deallocator import deallocate_img
from file_tools import save_images

from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from typing import List, Dict

from numpy import ndarray


def check_if_image_file(file: FileStorage) -> bool:
    """
    Checks, if file is image file based on ending of file. Currently supported: png, gif, jpg/ jpeg
    :param file: File from request body
    :return: Boolean, if file is an image file or not
    """
    return any([file.filename.endswith(image_format) for image_format in [".jpg", ".png", ".gif", ".jpeg"]])


def save_file_from_request(name: str, file: FileStorage) -> None:
    """
    Saves given file in img directory and saves meta information in model
    :param name: Name of image
    :param file: File from request body
    :return: None
    """
    if not check_if_image_file(file):
        return None
    data: Dict[str, any] = add_original_image(name, secure_filename(file.filename))
    directory: str = data['dir']
    file.save(directory)


def execute_image_deallocation(name: str, id: int, new_name: str, axis: int = 0) -> bool:
    """
    Executes image task with given data params, saves resulting images in directory and adds paths to meta.
    :param name: Name of image
    :param id: Id of image
    :param new_name: New  name of which image should be generated
    :param axis: 0 for horizontal and 1 for vertical
    :return: Boolean whether task was successful or not
    """
    data: Dict[str, any] = get_image(name, id)
    if data is None:
        return False
    imgs: List[ndarray] = deallocate_img(data, new_name, axis)
    directory: str = "new_img/%s/%i/%s/%i/" % (name, id, new_name, axis)
    directories: List[str] = save_images(imgs, directory)
    add_new_image(name, id, new_name, directories, axis)
    return True


def test():
    print(execute_image_deallocation("alex", 0, "eeeeee", 0))


if __name__ == '__main__':
    test()

