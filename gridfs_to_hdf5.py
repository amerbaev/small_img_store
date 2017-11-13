from pymongo import MongoClient
from gridfs import GridFS
import pandas as pd
import numpy as np
import h5py

if __name__ == '__main__':
    # db = MongoClient().small_img
    # fs = GridFS(db)
    # image_df = pd.DataFrame()
    #
    # for grid_out in fs.find():
    #     image_df = image_df.append(pd.DataFrame([[grid_out.read(), grid_out.metadata['xxhash64'], grid_out.filename]],
    #                                             columns=['data', 'xxhash64', 'filename'], dtype=np.str))
    # image_df.to_hdf('out/images.hdf5', key='images', mode='w', format='fixed')

    hdf5_file = h5py.File('out/images.hdf5', 'r')
    images = hdf5_file.get('images')
    print(*images.get('block0_values'))
