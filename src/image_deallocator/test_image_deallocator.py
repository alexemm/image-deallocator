from image_deallocator import deallocate_img
from file_tools import load_json, save_images


def test_image_deallocation():
    file = 'meta/data.json'
    name = 'alex'
    data = load_json(file)[name][0]
    print(data)
    new_name = 'aaaaaa'
    imgs = deallocate_img(data, new_name, 1)
    # for img in imgs:
    #     cv.imshow("EEEEE", img)
    #     cv.waitKey(0)
    save_images(new_name, imgs)


if __name__ == "__main__":
    test_image_deallocation()