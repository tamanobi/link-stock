"""
Link Stock をポーリングして変更があった場合はプロセスを実行する
"""
import os
import subprocess
import time
import urllib.request
from repositories import StockDB
from ext import LinkStockAPI, GalleryDL


while True:
    time.sleep(1)

    db = StockDB()
    con = db.get_connection()
    cur = db.get_cursor()
    db.create_table_if_not_exists()

    ids = LinkStockAPI.get()

    subete = db.get_all()
    atarashii = list(set(ids) - set(subete))
    if len(atarashii) > 0:
        print(atarashii)
    gdl = GalleryDL()
    for a in atarashii:
        url = a[1].replace("/ja/", "/")
        proc = gdl.run(url)
        print(proc.stderr)

        # import numpy as np
        # import pdqhash
        # from PIL import Image
        # im = Image.open("deadbeef.jpg")
        # np.asarray(im)
        # im_np = np.asarray(im)
        # hash_vector, quality = pdqhash.compute(im_np)

        db.insert(int(a[0]), a[1])
        db.commit()
    db.close()
