import h5py
import numpy as np
import xxhash
from collections import Counter


class Hdf5Store:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def __open_readwrite(self):
        if 'file' not in self.__dict__:
            self.file = h5py.File(self.file_path, 'r+')

    def close(self):
        if self.file:
            self.file.close()

    def create(self, size: int, image_chunks: int = 100, hash_chunks: int = None):
        if not hash_chunks:
            hash_chunks = size
        f = h5py.File(self.file_path, 'w')
        images = f.create_group('images')
        image_dset = images.create_dataset('img',
                                           shape=(size,),
                                           chunks=(image_chunks,),
                                           maxshape=(None,),
                                           dtype=np.dtype((np.void, 49152)))
        hash_dset = images.create_dataset('xxhash64',
                                          shape=(size,),
                                          chunks=(hash_chunks,),
                                          maxshape=(None,),
                                          dtype=np.dtype((np.void, 8)))
        image_dset.resize(size, axis=0)
        hash_dset.resize(size, axis=0)
        f.close()

    def resize(self, size: int):
        self.__open_readwrite()
        image_dset = self.file['/images/img']
        hash_dset = self.file['/images/xxhash64']
        image_dset.resize(size)
        hash_dset.resize(size)

    def put_image(self, index, image: bytes):
        xxhash64 = xxhash.xxh64(image).digest()
        self.__open_readwrite()
        image_dset = self.file['/images/img']
        hash_dset = self.file['/images/xxhash64']
        image_dset[index] = np.void(image)
        hash_dset[index] = np.void(xxhash64)

    def put_array(self, image_arr: np.array, hash_arr: np.array, start_index: int = 0):
        self.__open_readwrite()
        image_dset = self.file['/images/img']
        hash_dset = self.file['/images/xxhash64']
        image_dset[start_index:start_index + image_arr.size] = image_arr
        hash_dset[start_index:start_index + hash_arr.size] = hash_arr

    def find_collisions(self) -> list:
        self.__open_readwrite()
        hash_dset = self.file['/images/xxhash64']
        collisions = [item for item, count in Counter([value.tobytes() for value in hash_dset[:]]).most_common() if count > 1]
        return collisions

    def find_image_by_hash(self, xxh: np.void) -> bytes:
        self.__open_readwrite()
        images_grp = self.file['/images']
        index = np.argmax(images_grp['xxhash64'].value == xxh)
        result = images_grp['img'][index].tobytes() if index else b''
        return result

    def find_index_by_hash(self, xxh: np.void) -> int:
        self.__open_readwrite()
        hash_dset = self.file['/images/xxhash64']
        index = np.argmax(hash_dset.value == xxh)
        return index if index else -1

    def get_hash_by_index(self, index: int):
        self.__open_readwrite()
        hash_dset = self.file['/images/xxhash64']
        return hash_dset[index]
