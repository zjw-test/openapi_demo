# -*- coding: UTF-8 -*-
import json
import os

FILE_LOCATION = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


def read_json(filename, key):
    file = FILE_LOCATION + os.sep + "data" + os.sep + filename
    new = []
    with open(file, "r", encoding="utf-8") as f:
        for data in json.load(f).get(key):
            new.append(tuple(data.values())[1:])
        return new


def read_json_title(filename, key):
    file = FILE_LOCATION + os.sep + "data" + os.sep + filename
    new = []
    with open(file, "r", encoding="utf-8") as f:
        for data in json.load(f).get(key):
            x = list(data.values())
            y = x[0]
            new.append(y)
        return new
