import io
import numpy as np
from PIL import Image
import xxhash
import h5py
from tqdm import tqdm
import sys


def generate_img_to_hdf5(count: int):
    images = []
    hashes = []
    for i in tqdm(range(count)):
        image_bio = io.BytesIO()
        image_array = np.random.rand(128, 128, 4) * 255
        image = Image.fromarray(image_array.astype('uint8')).convert('RGBA')
        image.save(image_bio, format='png')
        images.append(image_bio.getvalue())
        hashes.append(xxhash.xxh64(image_bio.getvalue()).digest())
    with h5py.File('data/images.hdf5', 'w') as f:
        img_group = f.create_group('images')
        img_group.create_dataset('img', data=np.void(np.array(images)), dtype=np.dtype('V65790'))
        img_group.create_dataset('xxhash64', data=np.void(np.array(hashes)), dtype=np.dtype('V8'))


if __name__ == '__main__':
    generate_img_to_hdf5(1000)
