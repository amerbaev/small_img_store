import io
from multiprocessing import Pool

import numpy as np
from PIL import Image
from pymongo import MongoClient
from gridfs import GridFS


def generate_img_to_gridfs(name: str) -> str:
    image_bio = io.BytesIO()
    image_array = np.random.rand(128, 128, 3) * 255
    image = Image.fromarray(image_array.astype('uint8')).convert('RGBA')
    image.save(image_bio, format='png')
    fs = GridFS(MongoClient().small_img)
    file_id = fs.put(image_bio.getvalue(), filename=name + '.png')
    return str(file_id)


if __name__ == '__main__':
    with Pool(8) as p:
        print(p.map(generate_img_to_gridfs, [str(n) for n in range(1000)]))
