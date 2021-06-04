"""
Link Stock をポーリングして変更があった場合はプロセスを実行する
"""
import time
from repositories import StockDB, stock_db_context
from ext import LinkStockAPI, get_factory
import os

def get_not_saved_ids(remote_ids: list, local_ids: list) -> list:
    return list(set(remote_ids) - set(local_ids))


def normalize_url(url: str) -> str:
    return url.replace("/ja/", "/")


def normalize_url_list(list_) -> list:
    return [(id_, normalize_url(url)) for id_, url in list_]


if __name__ == "__main__":
    while True:
        gdl = get_factory()
        with stock_db_context() as db:
            db.create_table_if_not_exists()

            local_ids = db.get_all()
            remote_ids = LinkStockAPI.get()

            remote_ids = [(id_, normalize_url(url)) for id_, url in remote_ids]

            have_not_saved_ids = list(set(remote_ids) - set(local_ids))
            have_not_saved_ids = normalize_url_list(have_not_saved_ids)
            if len(have_not_saved_ids) > 0:
                print(have_not_saved_ids)
            for id_, url in have_not_saved_ids:
                url = normalize_url(url)
                proc = gdl.download(url)
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
