# encoding utf-8

import h5py
import numpy as np
from image_generator import generate_img_hash


def find_in_hdf5(images_group, xxhash) -> bytes:
    index = np.where(images_group['xxhash64'].value == xxhash)
    if index[0]:
        return images_group['img'][index[0][0]].tobytes()
    else:
        return b''


def init_hdf5(to_size):
    f = h5py.File('data/images.hdf5')
    images = f.create_group('images')
    image_arr, hash_arr = generate_img_hash(10)
    image_dset = images.create_dataset('img', data=image_arr, chunks=(100,), maxshape=(None,), dtype=image_arr.dtype)
    hash_dset = images.create_dataset('xxhash64', data=hash_arr, chunks=(1000,), maxshape=(None,), dtype=hash_arr.dtype)
    image_dset.resize(to_size, axis=0)
    hash_dset.resize(to_size, axis=0)
    f.close()


if __name__ == '__main__':
    init_hdf5(1000000)

    # f = h5py.File('data/images.hdf5', 'r')
    # image_dset = f['/images/img']
    # hash_dset = f['/images/xxhash64']
    #
    # with open('png/test.png', 'wb') as png_file:
    #     png_file.write(image_dset[1500])
    # f.close()

