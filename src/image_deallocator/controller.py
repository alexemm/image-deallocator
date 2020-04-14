from model import add_original_image, get_image, add_new_image
from image_deallocator import deallocate_img
from file_tools import save_images

from werkzeug.utils import secure_filename


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
    file.save(data['dir'])


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
    directory = "new_img/%s/%i/%s/" % (name, id, new_name)
    directories = save_images(imgs, directory)
    add_new_image(name, id, new_name, directories)
    return True


def test():
    print(execute_image_deallocation("lara", 0, "aaaaaaaa", 1))


if __name__ == '__main__':
    test()

