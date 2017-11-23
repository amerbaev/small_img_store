import numpy as np
import os
from PIL import Image
import xxhash
import h5py
from tqdm import tqdm
from multiprocessing import Pool


def generate_img_hash(count):
    images = np.empty(count, dtype=np.dtype((np.void, 49152)))
    hashes = np.empty(count, dtype=np.dtype((np.void, 8)))
    for i in range(count):
        image_array = np.random.randint(256, size=(128, 128, 3))
        image = Image.fromarray(image_array.astype('uint8')).convert('RGB').tobytes()
        images[i] = np.void(image)
        hashes[i] = np.void(xxhash.xxh64(image).digest())

    return images, hashes


def generate_img_with_pool(img_number: int,
                           file: str = 'images.hdf5',
                           generation_block: int = 1000,
                           processes: int = 8):
    gen_iterations = img_number // (processes * generation_block)
    p = Pool(processes)
    for i in tqdm(range(gen_iterations)):
        gen_img = p.map(generate_img_hash, [generation_block for _ in range(processes)])
        shift = i * generation_block * processes
        f = h5py.File('data' + os.sep + file, 'r+')
        image_dset = f['/images/img']
        hash_dset = f['/images/xxhash64']
        for j, (images_arr, hashes_arr) in enumerate(gen_img):
            for k in range(len(images_arr)):
                total_index = shift + j * generation_block + k
                try:
                    image_dset[total_index] = images_arr[k]
                    hash_dset[total_index] = hashes_arr[k]
                except Exception as e:
                    f.close()
                    raise e
        f.close()
