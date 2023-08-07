import os
from material_zui.image.data import IMG_EXT
import requests

# def get_image_sizes(directory_path: str) -> list[dict[{'name': str, 'width': int, 'height': int}]]:
#     images = get_image(directory_path)
#     images_name = get_image_name(directory_path)
#     return [{'name': images_name[index], 'width':image.width, 'height':image.height}
#             for index, image in enumerate(images)]


# def get_image(directory_path: str) -> list[Image.Image]:
#     images_name = get_image_name(directory_path)
#     # print(images_name)
#     return list(map(lambda file_name: Image.open(os.path.join(
#         directory_path, file_name)), images_name))
# def get_image(directory_path: str) -> list[ZuiImage]:
#     images_name = get_image_name(directory_path)
#     images = [Image.open(os.path.join(directory_path, file_name))
#               for file_name in images_name]
#     return [{'image': image, 'name': images_name[index], 'ext': image.format or '', 'width':image.width, 'height':image.height} for index, image in enumerate(images)]


def get_image_name(directory_path: str) -> list[str]: return list(filter(lambda file_name: file_name.endswith(
    IMG_EXT), os.listdir(directory_path)))


def download(url: str, path: str) -> None:
    '''Download image by url to path'''
    response = requests.get(url)
    with open(path, "wb") as f:
        f.write(response.content)
