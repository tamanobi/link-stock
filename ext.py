import urllib.request
import json


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