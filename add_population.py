#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from app.models import data as d, population as p


def main():

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

    print(f"セーブ{data.maxsave}⇒{data.maxsave + 1}")
    data.maxsave += 1

    print(f"最新日付：{data.cur_date}")
    newdate = input("新しい日付：")

    error = 0

    for town in sorted(data.active_towns, key=lambda x: x.name):

        usr_in = input(f"{town.name}の人口：").split("\t")

        if len(usr_in) == 1:
            name = town.name
            pop = usr_in[0]
        elif len(usr_in) == 2:
            name = usr_in[0]
            pop = usr_in[1]

        if name == town.name or name == f"{town}":
            data.populations.append(p.Population([data.populations[-1].uid + 1,
                                                  data.maxsave, newdate,
                                                  town, pop], data))
        else:
            error += 1

    if error != 0:
        print("There is something wrong, investigate please.")
        return error

    data.update_data()
    data.update_datafile()

    print("")


if __name__ == "__main__":
    main()
