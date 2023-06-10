from PIL import Image
import numpy as np
from scipy import ndimage

WIDTH = 75
HEIGHT = 50

def new_sized(file_name):
    with Image.open(file_name) as img:
        img.load()
    w, h = img.size
    k_w, k_h = w / WIDTH, h / HEIGHT
    if k_w > k_h:
        new_h = min(int(h / k_w), h)
        new_size = (min(WIDTH, int(w * new_h / h)), new_h)
    else:
        new_w = min(int(w / k_h), w)
        new_size = (new_w, min(HEIGHT, int(h * new_w / w)))
    conv = img.convert('1')
    return conv.resize(new_size), new_size


def shift(positions, size):
    shift_w = (WIDTH - size[0]) // 2
    shift_h = (HEIGHT - size[1]) // 2
    return set((x + shift_h, y + shift_w) for x, y in positions)


def image_prepare(file_name):
    img, size = new_sized(file_name)
    bits_array = np.asarray(img)
    start_positions = np.nonzero(bits_array == False)
    return shift(set(zip(*start_positions)), size)


if __name__ == '__main__':
    print(image_prepare(r'.\images\you_head.jpg'))
