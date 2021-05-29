import urllib.request
import json
import subprocess
from constants import GALLERY_DL


class APIError(Exception):
    def __init__(self, *args, **kwargs):
        self.message = "APIサーバーエラー"
        super().__init__(*args, **kwargs)


class LinkStockAPI:
    @classmethod
    def get(cls):
        ids = []
        req = urllib.request.Request(url="https://cryptic-wildwood-50649.herokuapp.com/get")
        with urllib.request.urlopen(req) as res:
            if res is None:
                raise APIError()
            if res.status != 200:
                raise APIError()
            records = json.loads(res.read())["record"]
            ids = [
                (rec["id"], rec.get("url"))
                for rec in records
                if rec.get("url") is not None and "?tags" not in rec.get("url")
            ]
        return ids

class GalleryDL():
    def run(self, url):
        cmd = f"{GALLERY_DL} --config ./gallery-dl.conf {url}"
        print(cmd)
        proc = subprocess.run(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
        )
        return proc
