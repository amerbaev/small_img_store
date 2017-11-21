import io
import numpy as np
from PIL import Image
import xxhash
import h5py
from tqdm import tqdm
from multiprocessing import Pool

PROC = 8

COUNT = 1000000
BLOCK = 1000


def generate_img_hash(count):
    images = np.empty(count, dtype=np.dtype((np.void, 49353)))
    hashes = np.empty(count, dtype=np.dtype((np.void, 8)))
    for i in range(count):
        image_bio = io.BytesIO()
        image_array = np.random.randint(256, size=(128, 128, 3))
        image = Image.fromarray(image_array.astype('uint8')).convert('RGB')
        image.save(image_bio, format='png')
        images[i] = np.void(image_bio.getvalue())
        hashes[i] = np.void(xxhash.xxh64(image_bio.getvalue()).digest())

    return images, hashes


if __name__ == '__main__':
    gen_iterations = COUNT // (PROC * BLOCK)
    p = Pool(PROC)

    for i in tqdm(range(gen_iterations)):
        gen_img = p.map(generate_img_hash, [BLOCK for _ in range(PROC)])
        shift = i * BLOCK * PROC
        f = h5py.File('data/images.hdf5', 'r+')
        image_dset = f['/images/img']
        hash_dset = f['/images/xxhash64']
        for j, (images_arr, hashes_arr) in enumerate(gen_img):
            for k in range(len(images_arr)):
                total_index = shift + j * BLOCK + k
                try:
                    image_dset[total_index] = images_arr[k]
                    hash_dset[total_index] = hashes_arr[k]
                except Exception as e:
                    f.close()
                    print(e)
        f.close()
