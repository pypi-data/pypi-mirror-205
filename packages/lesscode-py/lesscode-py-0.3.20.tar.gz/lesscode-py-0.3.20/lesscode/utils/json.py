import datetime
import importlib
import json
from decimal import Decimal

try:
    bson = importlib.import_module("bson")

except ImportError as e:
    raise Exception(f"pymongo is not exist,run:pip install pymongo==3.13.0")


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, bson.ObjectId):
            return str(o)
        elif isinstance(o, datetime.datetime):
            return str(o)
        elif isinstance(o, bytes):
            return str(o, encoding="utf-8")
        elif isinstance(o, set):
            return list(o)
        elif isinstance(o, Decimal):
            return str(o)
        return json.JSONEncoder.default(self, o)
