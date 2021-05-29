"""
Link Stock をポーリングして変更があった場合はプロセスを実行する
"""
import os
import subprocess
import time
import urllib.request
from constants import GALLERY_DL
from repositories import StockDB
from ext import LinkStockAPI


import sqlite3

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
    for a in atarashii:
        url = a[1].replace("/ja/", "/")
        cmd = f"{GALLERY_DL} --config ./gallery-dl.conf {url}"
        proc = subprocess.run(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
        )
        print(cmd)
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
