# encoding utf-8

import h5py
import numpy as np
import os

import image_generator as img_gen


def find_image_by_hash(images_group, xxh) -> bytes:
    index = np.argmax(images_group['xxhash64'].value == xxh)
    if index:
        return images_group['img'][index].tobytes()
    else:
        return b''


def find_index_by_hash(dset, xxh) -> int:
    index = np.argmax(dset.value == xxh)
    if index:
        return index
    else:
        return -1


def init_hdf5(size: int, image_chunks: int = 100, hash_chunks: int = None):
    if not os.path.exists('data'):
        os.makedirs('data')
    if not hash_chunks:
        hash_chunks = size
    f = h5py.File('data/images.hdf5', 'w')
    images = f.create_group('images')
    image_arr, hash_arr = img_gen.generate_img_hash(10)
    image_dset = images.create_dataset('img',
                                       data=image_arr,
                                       chunks=(image_chunks,),
                                       maxshape=(None,),
                                       dtype=image_arr.dtype)
    hash_dset = images.create_dataset('xxhash64',
                                      data=hash_arr,
                                      chunks=(hash_chunks,),
                                      maxshape=(None,),
                                      dtype=hash_arr.dtype)
    image_dset.resize(size, axis=0)
    hash_dset.resize(size, axis=0)
    f.close()


if __name__ == '__main__':
    img_number = 10000000
    print('Создание файла')
    init_hdf5(img_number)
    print('Генерация изображений')
    img_gen.generate_img_with_pool(img_number)
