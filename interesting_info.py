#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import re
from app.models import data as d
from datetime import datetime


def main(argv):

    if len(argv) != 1 and len(argv) > 1:
        exit(f"{sys.argv[0]} <save no.>\nsave no. - default is max save")
    elif len(argv) == 1:
        try:
            save = int(argv[0])
        except ValueError:
            exit(f"{sys.argv[0]} <save no.>\nsave no. - default is max save")

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

    if len(argv) == 1:
        data.maxsave = save

    print(f"セーブ{data.maxsave}")

    if "年" in data.dates[-1]:
        print(datetime.strptime(data.dates_np[-1], "%Y年%m月%d日").date())
    else:
        print(datetime.strptime(data.dates[-1], "%Y/%m/%d").date())

    print(f"都市数：{len(data.active_towns)}")

    if data.maxsave >= 1:
        total = 0
        for town in data.active_towns:
            total += town.cur_population

            if data.maxsave > 1:
                try:
                    if town.cur_population/town.population[-2] > 1.1 \
                            or town.cur_population/town.population[-2] < .9:
                        print(f"注目 {town} 人口大きく変わりました")
                except ZeroDivisionError:
                    print(f"新しい都市 {town}")

        print(f"人口：{fn(total)}人")

        print(10*"=")

        for prefecture in sorted(data.prefectures.values(),
                                 key=lambda x: x.cur_population, reverse=True):
            print(f"{prefecture.name}: {fn(prefecture.cur_population)}人 "
                  f" {prefecture.cur_population/total*100:.2f}%%")

        print(10*"=")

        biggest_cities = {}
        wards = {}
        for town in data.active_towns:
            if not town.ward:
                biggest_cities[town.name] = [town.cur_population, [town]]
            else:
                try:
                    biggest_cities[town.city][0] += town.cur_population
                    biggest_cities[town.city][1].append(town)
                    wards[town.city] += 1
                except KeyError:
                    biggest_cities[town.city] = [town.cur_population, [town]]
                    wards[town.city] = 1

        for big_city, (pop, city) in sorted(biggest_cities.items(),
                                            key=lambda x: x[1][0],
                                            reverse=True)[:10]:
            if len(city) != 1:
                print(f"{city[0].prefecture} - {big_city}：{fn(pop)}人 "
                      f"({wards[big_city]}区) {pop/total*100:.2f}%")
            else:
                print(f"{city[0].prefecture} - {big_city}：{fn(pop)}人 "
                      f"{pop/total*100:.2f}%")

        print(10*"=")

        daitokai = {}

        for town in data.active_towns:
            if town.ward:
                try:
                    daitokai[town.city][0] += town.cur_population
                    daitokai[town.city][1].append(town)
                except KeyError:
                    daitokai[town.city] = [town.cur_population, [town]]

        for city, (totpop, wards) in sorted(daitokai.items(),
                                            key=lambda x: x[1], reverse=True):
            print(f"{city}：{fn(totpop)}人 {totpop/total*100:.2f}%")
            for ward in sorted(wards, key=lambda x: x.cur_population,
                               reverse=True):
                print(f"  {ward.ward}区：{fn(ward.cur_population)}人 "
                      f"{ward.cur_population/totpop*100:.2f}%")

        print(10*"=")

        prefectures = {prefecture: 0 for prefecture in
                       data.prefectures.values()}

        for prefecture in prefectures.keys():
            for town in prefecture.towns:
                if town in data.active_towns:
                    prefectures[prefecture] += 1

        for prefecture, amount in prefectures.items():
            print(f"{prefecture}：{amount}")

        print(10*"=")

    if data.maxsave > 2:

        for town in data.active_towns:
            if not town.growth_stopped and \
                    1 - town.cur_population/town.planned < 0:
                print(f"注意 {town} 人口は計画人口に超えました")
                print(f"現在の人口 {fn(town.cur_population)}人 - 計画人口 "
                      f"{fn(town.planned)}人")
            elif not town.growth_stopped and \
                    abs(1 - town.cur_population/town.planned) < .1:
                print(f"注意 {town} 人口は計画人口に近づいています")
                print(f"現在の人口 {fn(town.cur_population)}人 - 計画人口 "
                      f"{fn(town.planned)}人")


def fn(n):
    return re.sub(r"(\d)(?=(\d{4})+(?!\d))", r"\1 ", str(n))


if __name__ == "__main__":
    main(sys.argv[1:])
