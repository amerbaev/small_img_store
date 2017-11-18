# encoding utf-8

import h5py
import numpy as np


if __name__ == '__main__':
    f = h5py.File('data/images.hdf5', 'r')
    image_files = f['/images/img']

    print(image_files[0].tobytes())
