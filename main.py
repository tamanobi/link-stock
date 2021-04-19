"""
Link Stock をポーリングして変更があった場合はプロセスを実行する
"""
import os
import subprocess
import time
import urllib.request
import json

import sqlite3

while True:
    time.sleep(1)

    con = sqlite3.connect('image.db')
    cur = con.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS saved
            (
                id integer
                , url text
                , created_at TEXT NOT NULL DEFAULT (DATETIME('now', 'localtime'))
            )
    ''')

    ids = []
    req = urllib.request.Request(url="https://cryptic-wildwood-50649.herokuapp.com/get")
    with urllib.request.urlopen(req) as res:
        if res is None:
            exit(1)
        if res.status != 200:
            exit(1)
        records = json.loads(res.read())["record"]
        ids = [(rec["id"], rec.get("url")) for rec in records if rec.get("url") is not None and "?tags" not in rec.get("url")]

    cur.execute('SELECT id, url FROM saved')
    subete = [(x[0], x[1]) for x in cur.fetchall()]
    atarashii = list(set(ids) - set(subete))
    if len(atarashii) > 0:
        print(atarashii)
    for a in atarashii:
        url = a[1].replace("/ja/", "/")
        GALLERY_DL = "/home/tamanobi/.anyenv/envs/pyenv/versions/3.8.5/bin/gallery-dl"
        cmd = f"{GALLERY_DL} --config ./gallery-dl.conf {url}"
        proc = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        print(cmd)
        print(proc.stderr)

        cur.execute('''
            INSERT INTO saved (id, url) VALUES (?, ?)
        ''', [int(a[0]), a[1]])
        con.commit()
    con.close()