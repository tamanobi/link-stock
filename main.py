"""
Link Stock をポーリングして変更があった場合はプロセスを実行する
"""
import time
from repositories import StockDB
from ext import LinkStockAPI, GalleryDL


def get_not_saved_ids(remote_ids: list, local_ids: list) -> list:
    return list(set(remote_ids) - set(local_ids))


while True:
    time.sleep(1)

    db = StockDB()
    con = db.get_connection()
    cur = db.get_cursor()
    db.create_table_if_not_exists()

    remote_ids = LinkStockAPI.get()

    local_ids = db.get_all()
    not_saved_ids = get_not_saved_ids(remote_ids, local_ids)
    if len(not_saved_ids) > 0:
        print(not_saved_ids)
    gdl = GalleryDL()
    for id_, url in not_saved_ids:
        url = url.replace("/ja/", "/")
        proc = gdl.run(url)
        print(proc.stderr)

        # import numpy as np
        # import pdqhash
        # from PIL import Image
        # im = Image.open("deadbeef.jpg")
        # np.asarray(im)
        # im_np = np.asarray(im)
        # hash_vector, quality = pdqhash.compute(im_np)

        db.insert(int(id_), url)
        db.commit()
    db.close()
