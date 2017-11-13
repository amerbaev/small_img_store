from multiprocessing import Pool

from pymongo import MongoClient
from gridfs import GridFS
import xxhash


def xxhash_gridin(filename):
    db = MongoClient().small_img
    gridfs = GridFS(db)
    file_out = gridfs.find_one(filter={'filename': filename})
    file_xxhash = xxhash.xxh64(file_out.read()).hexdigest()
    update_result = db.fs.files.update_one({"_id": file_out._id}, {'$set': {'metadata.xxhash64': file_xxhash}})
    return update_result.modified_count


if __name__ == '__main__':
    fs = GridFS(MongoClient().small_img)
    with Pool(8) as p:
        result = p.map(xxhash_gridin, fs.list())
    print(sum(result))
