# encoding utf-8

import numpy as np
from timeit import timeit

import image_generator as img_gen
from hdf5_store import Hdf5Store


if __name__ == '__main__':
    file = 'data/images.hdf5'

    print('Создание класса')
    store = Hdf5Store(file)
    img_number = 10000000
    # print('Создание файла')
    # store.create(img_number)
    #
    # print('Генерация изображений')
    # img_gen.generate_img_with_pool(img_number, store)

    print('Загрузка хешей в память')
    store.load_hashes()
    print('Хеши успешно загружены')
    print('Время поиска хеша:', "{0:.8f}".format(np.mean([timeit('store.find_index_by_hash(xxhash)',
                                                                 setup='xxhash = store.get_hash_by_index(np.random.randint(img_number))',
                                                                 globals=globals(),
                                                                 number=1)
                                                          for _ in range(10000)])))
    print('Коллизии: ', store.find_collisions())

    store.close()
