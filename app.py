# encoding utf-8

import h5py
import numpy as np


def find_in_hdf5(images_group, xxhash) -> bytes:
    index = np.where(images_group['xxhash64'].value == xxhash)
    if index[0]:
        return images_group['img'][index[0][0]].tobytes()
    else:
        return b''


if __name__ == '__main__':
    f = h5py.File('data/images.hdf5', 'r')
    images = f['/images']

    xxhash = images['xxhash64'][30]
    print(find_in_hdf5(images, np.void(xxhash)))
    print(find_in_hdf5(images, np.void(b'notexsit')))
