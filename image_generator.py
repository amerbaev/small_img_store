import numpy as np
from PIL import Image
import xxhash
from tqdm import tqdm
from multiprocessing import Pool
from hdf5_store import Hdf5Store


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
                           store: Hdf5Store,
                           generation_block: int = 1000,
                           processes: int = 8):
    gen_iterations = img_number // (processes * generation_block)
    p = Pool(processes)
    for i in tqdm(range(gen_iterations)):
        gen_img = p.map(generate_img_hash, [generation_block for _ in range(processes)])
        shift = i * generation_block * processes
        for j, (images_arr, hashes_arr) in enumerate(gen_img):
            index = shift + j * generation_block
            store.put_array(images_arr, hashes_arr, index)