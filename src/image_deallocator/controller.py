from model import add_original_image, get_image, add_new_image
from image_deallocator import deallocate_img
from file_tools import save_images

from werkzeug.utils import secure_filename
from os import makedirs, path, replace


def check_if_image_file(file) -> bool:
    """

    :param file:
    :return:
    """
    return any([file.filename.endswith(image_format) for image_format in [".jpg", ".png", ".gif"]])


def save_file_from_request(name: str, file):
    """

    :param name:
    :param file:
    :return:
    """
    if not check_if_image_file(file):
        return
    data = add_original_image(name, secure_filename(file.filename))
    directory = data['dir']
    file.save(directory)


def execute_image_deallocation(name: str, id: int, new_name: str, axis: int = 0) -> bool:
    """

    :param name:
    :param id:
    :param new_name:
    :param axis:
    :return:
    """
    data = get_image(name, id)
    if data is None:
        return False
    imgs = deallocate_img(data, new_name, axis)
    directory = "new_img/%s/%i/%s/%i/" % (name, id, new_name, axis)
    directories = save_images(imgs, directory)
    add_new_image(name, id, new_name, directories, axis)
    return True


def test():
    print(execute_image_deallocation("alex", 0, "eeeeee", 0))


if __name__ == '__main__':
    test()

