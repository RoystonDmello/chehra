"""
Module for functions to retrieve image from nodemcu board
"""
import requests
from urllib.parse import urljoin
from PIL import Image
import numpy as np
import io

RESET = 'clear'
CLICK = 'submit'
IMAGE = '1.jpg'


def retrieve_image(url):
    """
    Given an image url gets the image in the form of a numpy array
    :param url: String, url from which image has to be retrieved
    :return: Numpy array, array of image
    """

    r = requests.get(url)
    img = Image.open(io.BytesIO(r.content))

    return np.array(img)


def class_click(url_list):
    """
    Given a list of base urls it clicks the pictures using those cameras and
    returns a list of their arrays
    :param url_list: List, base urls of cameras
    :return: list, list of images
    """

    imgs = []

    for base_url in url_list:
        reset_url = urljoin(base_url, RESET)
        click_url = urljoin(base_url, CLICK)
        retrieve_url = urljoin(base_url, IMAGE)

        requests.get(reset_url)
        requests.get(click_url)

        img = retrieve_image(retrieve_url)

        imgs.append(img)

    return imgs
