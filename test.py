#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

# import numpy as np
import re

from app.models import data as d


def main(argv):
    data_path = os.path.abspath("data")
    maps = [name for name in os.listdir(data_path) if
            os.path.isdir(os.path.abspath(os.path.join(data_path, name)))]

    for i, mapname in enumerate(maps):
        print(f"{i}: {mapname}")

    mess = "マップを選択してください、マップの前にある数字を入力してください："

    while True:
        try:
            mapid = int(input(mess))

            if mapid in range(len(maps)):
                break
            else:
                print()
        except ValueError:
            pass

    data = d.Data(f"data/{maps[mapid]}")

    print(f"セーブ{data.maxsave}")

    city = input("探す都市：")

    # total = 0

    # cities = ["中原", "大垣", "白野", "宮木", "羽島", "海沢", "高岡"]

    for town in sorted(data.active_towns, key=lambda x: x.name):
        if city in town.name:
            print(f"{town}：{format_number(town.population[-1])}人")
            exit()
            break
    print(f"{city}を見つかりませんでした")


def format_number(n):
    return re.sub(r"(\d)(?=(\d{4})+(?!\d))", r"\1 ", str(n))


if __name__ == "__main__":
    main(sys.argv[1:])
