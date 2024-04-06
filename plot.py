#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys
import numpy
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm, rcParams
from datetime import datetime
from app.models import data as d
# from app.script import date_conversion as dc


def main(argv):

    data = map_select()

    fonts = fm.findSystemFonts()
    for font in fonts:
        if "Takao" in font:
            prop = fm.FontProperties(fname=font)
            break
        else:
            prop = fm.FontProperties()

    rcParams['font.family'] = prop.get_name()

    save_no_list = [i for i in range(1, data.maxsave + 1)]

    lang = data.language
    mapname = data.mapname[0]
    try:
        mapname_en = data.mapname[1]
    except IndexError:
        mapname_en = None
    subdiv = data.subdiv[0]
    try:
        subdiv_en = data.subdiv[1]
    except IndexError:
        subdiv_en = None
    datesave = not False
    logplot = not True

    xlabel = "Save"
    ylabel = "log$_{10}$(population)"
    maxtop = 10

    if lang == "JP":
        date_list = [datetime.strptime(date, "%Y年%m月%d日").date()
                     for date in data.dates_np]
        title1 = f"{mapname}都市の人口/{mapname_en} City Population"
        title2 = f"{mapname}{subdiv}の人口/{mapname_en} {subdiv_en} Population"
        xlabel = "セーブ/" + xlabel
        ylabel = "log$_{10}$(人口 [人])/" + ylabel
        separator = 4
    else:
        date_list = [datetime.strptime(date, "%Y/%m/%d").date()
                     for date in data.dates]
        title1 = f"{mapname} Population per City"
        title2 = f"{mapname} Population per {subdiv}"
        separator = 3

    plt.figure()

    index = 0

    towns = sorted([town for town in data.towns if not town.ward],
                   key=lambda x: x.population[-1], reverse=True)[:maxtop]

    for town in towns:
        pophist = town.population

        if datesave:
            plt.plot(date_list, pophist, label=town.name)
        else:
            plt.plot(save_no_list, pophist, label=town.name)

        index += 1

    plt.title(title1, fontproperties=prop)
    if datesave:
        plt.xlabel("Year")
        plt.xlim(date_list[0], date_list[-1])
    else:
        plt.xlabel(xlabel, fontproperties=prop)
        plt.xlim(0, save_no_list[-1])
    if logplot:
        plt.ylabel(ylabel, fontproperties=prop)
        plt.yscale("log")
    else:
        plt.ylabel("Population")
        plt.ylim(0,)
        plt.gca().yaxis.set_major_formatter(lambda x, pos:
                                            format_number(int(x), separator))
    plt.legend(prop={'size': 10})
    plt.tight_layout()
    plt.savefig("test1.png")

    plt.figure()
    plt.title(title2, fontproperties=prop)

    total_population = [0 for _ in range(data.maxsave)]

    legend = ["Total"]

    logplot = not False

    h = []

    for prefecture in data.prefectures.values():
        pophist = prefecture.population

        for i, value in enumerate(pophist):
            total_population[i] += value

        legend.append(prefecture.name)

        if datesave:
            h.append(plt.plot(date_list, pophist)[0])
        else:
            h.append(plt.plot(save_no_list, pophist)[0])

    if datesave:
        h.insert(0, plt.plot(date_list, total_population, color="black")[0])
    else:
        h.insert(0, plt.plot(save_no_list, total_population, color="black")[0])

    plt.gca().legend(handles=h, labels=legend, prop=prop)
    if datesave:
        plt.xlabel("Year")
        plt.xlim(date_list[0], date_list[-1])
    else:
        plt.xlabel(xlabel, fontproperties=prop)
        plt.xlim(0, save_no_list[-1])
    if logplot:
        plt.ylabel(ylabel, fontproperties=prop)
        plt.yscale("log")
    else:
        plt.ylabel("Population")
        plt.ylim(0,)
        plt.gca().yaxis.set_major_formatter(lambda x, pos:
                                            format_number(int(x), separator))

    plt.tight_layout()
    plt.savefig("test2.png")


def format_number(n, x):
    return re.sub(fr"(\d)(?=(\d{{{x}}})+(?!\d))", r"\1 ", str(n))


def map_select():
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

    return data


if __name__ == "__main__":
    main(sys.argv[1:])
