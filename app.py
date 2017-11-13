# encoding utf-8

import os
from multiprocessing import Pool


from pymongo import MongoClient
import gridfs


# fsbuck = gridfs.GridFSBucket(db)


def get_file(name):
    db = MongoClient().small_img
    fs = gridfs.GridFS(db)
    return fs.get_last_version(name).md5


def get_files():
    p = Pool(8)
    test = p.map(get_file, [filename for filename in os.listdir('png')])
    print(test)


if __name__ == '__main__':
    db = MongoClient().small_img
    fs = gridfs.GridFS(db)
    hashes = []
    for grid_out in fs.find():
        print(grid_out.metadata)
    # print(len(hashes))