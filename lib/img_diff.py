from PIL import Image, ImageChops, ImageDraw
import math
import operator
import os
from functools import reduce

TYPE_EQUAL = 'equal'
TYPE_RMS = 'rms'


def comapre(image_path_1, image_path_2, mode=TYPE_EQUAL):
    with Image.open(image_path_1) as im1, Image.open(image_path_2) as im2:

        if mode == TYPE_RMS:
            diff = rmsdiff(im1, im2)
        else:
            diff = equal(im1, im2)

        if diff:
            im2_draw = ImageDraw.Draw(im2)
            im2_draw.rectangle(diff, outline=(255, 0, 0))
            path_split = os.path.splitext(image_path_2)
            file_path = f'{path_split[0]}-diff{path_split[1]}'
            im2.save(file_path)
        else:
            file_path = image_path_2

        return {'result': diff, 'file_path': file_path}


def compare_all(images_paths_1, images_paths_2, mode=TYPE_EQUAL):
    if len(images_paths_1) != len(images_paths_2):
        raise Exception('images number not equals')

    result = []
    for i in range(len(images_paths_1)):
        result.append(comapre(images_paths_1[i], images_paths_2[i], mode))

    return result


def rmsdiff(im1, im2, threshhold=0):
    "Calculate the root-mean-square difference between two images"

    h = ImageChops.difference(im1, im2).histogram()

    # calculate rms
    rms = math.sqrt(reduce(operator.add,
                           map(lambda h, i: h*(i**2), h, range(256))
                           ) / (float(im1.size[0]) * im1.size[1]))

    if rms > threshhold:
        return ImageChops.difference(im1, im2).getbbox()
    else:
        return None


def equal(im1, im2):
    return ImageChops.difference(im1, im2).getbbox()
