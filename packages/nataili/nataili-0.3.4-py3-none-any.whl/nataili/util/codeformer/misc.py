import os
from urllib.parse import urlparse

import cv2
import numpy as np
import torch
from PIL import Image
from torch.hub import download_url_to_file, get_dir


def imwrite(img, file_path, params=None, auto_mkdir=True):
    """Write image to file.

    Args:
        img (ndarray): Image array to be written.
        file_path (str): Image file path.
        params (None or list): Same as opencv's :func:`imwrite` interface.
        auto_mkdir (bool): If the parent folder of `file_path` does not exist,
            whether to create it automatically.

    Returns:
        bool: Successful or not.
    """
    if auto_mkdir:
        dir_name = os.path.abspath(os.path.dirname(file_path))
        os.makedirs(dir_name, exist_ok=True)
    return cv2.imwrite(file_path, img, params)


def load_file_from_url(url, model_dir=None, progress=True, file_name=None):
    """Ref:https://github.com/1adrianb/face-alignment/blob/master/face_alignment/utils.py"""
    if model_dir is None:
        hub_dir = get_dir()
        model_dir = os.path.join(hub_dir, "checkpoints")
    os.makedirs(model_dir, exist_ok=True)
    parts = urlparse(url)
    filename = os.path.basename(parts.path)
    if file_name is not None:
        filename = file_name
    cached_file = os.path.abspath(os.path.join(model_dir, filename))
    if not os.path.exists(cached_file):
        print(f'Downloading: "{url}" to {cached_file}\n')
        download_url_to_file(url, cached_file, hash_prefix=None, progress=progress)
    return cached_file


def img2tensor(imgs, bgr2rgb=True, float32=True):
    """Numpy array to tensor.

    Args:
        imgs (list[ndarray] | ndarray): Input images.
        bgr2rgb (bool): Whether to change bgr to rgb.
        float32 (bool): Whether to change to float32.

    Returns:
        list[tensor] | tensor: Tensor images. If returned results only have
            one element, just return tensor.
    """

    def _totensor(img, bgr2rgb, float32):
        if img.shape[2] == 3 and bgr2rgb:
            if img.dtype == "float64":
                img = img.astype("float32")
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = torch.from_numpy(img.transpose(2, 0, 1))
        if float32:
            img = img.float()
        return img

    if isinstance(imgs, list):
        return [_totensor(img, bgr2rgb, float32) for img in imgs]
    else:
        return _totensor(imgs, bgr2rgb, float32)


def is_gray(img, threshold=10):
    img = Image.fromarray(img)
    if len(img.getbands()) == 1:
        return True
    img1 = np.asarray(img.getchannel(channel=0), dtype=np.int16)
    img2 = np.asarray(img.getchannel(channel=1), dtype=np.int16)
    img3 = np.asarray(img.getchannel(channel=2), dtype=np.int16)
    diff1 = (img1 - img2).var()
    diff2 = (img2 - img3).var()
    diff3 = (img3 - img1).var()
    diff_sum = (diff1 + diff2 + diff3) / 3.0
    if diff_sum <= threshold:
        return True
    else:
        return False


def rgb2gray(img, out_channel=3):
    r, g, b = img[:, :, 0], img[:, :, 1], img[:, :, 2]
    gray = 0.2989 * r + 0.5870 * g + 0.1140 * b
    if out_channel == 3:
        gray = gray[:, :, np.newaxis].repeat(3, axis=2)
    return gray


def bgr2gray(img, out_channel=3):
    b, g, r = img[:, :, 0], img[:, :, 1], img[:, :, 2]
    gray = 0.2989 * r + 0.5870 * g + 0.1140 * b
    if out_channel == 3:
        gray = gray[:, :, np.newaxis].repeat(3, axis=2)
    return gray
