"""
Link Stock をポーリングして変更があった場合はプロセスを実行する
"""
import time
from repositories import StockDB, stock_db_context
from ext import LinkStockAPI, GalleryDL


def get_not_saved_ids(remote_ids: list, local_ids: list) -> list:
    return list(set(remote_ids) - set(local_ids))


def normalize_url(url: str) -> str:
    return url.replace("/ja/", "/")


while True:
    gdl = GalleryDL()
    with stock_db_context() as db:
        db.create_table_if_not_exists()

        local_ids = db.get_all()
        remote_ids = LinkStockAPI.get()

        not_saved_ids = get_not_saved_ids(remote_ids, local_ids)
        if len(not_saved_ids) > 0:
            print(not_saved_ids)

        for id_, url in not_saved_ids:
            url = normalize_url(url)
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
    time.sleep(1)
