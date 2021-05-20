"""
Link Stock をポーリングして変更があった場合はプロセスを実行する
"""
import os
import subprocess
import time
import urllib.request
import json
from constants import GALLERY_DL
from repositories import StockDB

import sqlite3

while True:
    time.sleep(1)

    cur = StockDB.get_cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS saved
            (
                id integer
                , url text
                , created_at TEXT NOT NULL DEFAULT (DATETIME('now', 'localtime'))
            )
    """
    )

    ids = []
    req = urllib.request.Request(url="https://cryptic-wildwood-50649.herokuapp.com/get")
    with urllib.request.urlopen(req) as res:
        if res is None:
            exit(1)
        if res.status != 200:
            exit(1)
        records = json.loads(res.read())["record"]
        ids = [
            (rec["id"], rec.get("url"))
            for rec in records
            if rec.get("url") is not None and "?tags" not in rec.get("url")
        ]

    cur.execute("SELECT id, url FROM saved")
    subete = [(x[0], x[1]) for x in cur.fetchall()]
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

        cur.execute(
            """
            INSERT INTO saved (id, url) VALUES (?, ?)
        """,
            [int(a[0]), a[1]],
        )
        con.commit()
    con.close()
