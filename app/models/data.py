#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
version: python 3+
data.py defines the data model used for this app
Dani van Enk
"""
import os
import csv
import dotenv as dot

from .town import Town
from .population import Population
from .prefecture import Prefecture


class Data:
    def __init__(self, folder):
        self._folder = os.path.abspath(folder)
        self._towndata_file = \
            os.path.abspath(os.path.join(self._folder, "towndata.csv"))
        self._populationdata_file = \
            os.path.abspath(os.path.join(self._folder, "populationdata.csv"))

        dot.load_dotenv(os.path.join(self._folder, ".env"))

        self._period_name = os.getenv("name_period")
        self._start_period = os.getenv("start_period")
        self._language = os.getenv("lang")
        self._mapname = os.getenv("name")
        self._subdiv = os.getenv("subdivision")

        self.load_data()

    def load_data(self):
        with open(self._towndata_file) as file:
            reader = csv.reader(file, delimiter=",")
            self._town_header = next(reader)

            self._towns = []

            for row in reader:
                if row == self._town_header:
                    continue
                self._towns.append(Town(row, self))

        with open(self._populationdata_file) as file:
            reader = csv.reader(file, delimiter=",")
            self._population_header = next(reader)

            self._populations = []

            for row in reader:
                self._populations.append(Population(row, self))

            self._dates = []

            save = 0

            for population in self._populations:
                if save != population.save:
                    self._dates.append(population.date)
                    save += 1

        try:
            self.maxsave = self._populations[-1].save
            self.cur_date = self._populations[-1].date
        except IndexError:
            self.maxsave = 0
            self.cur_date = ""

        self._prefectures = {str(prefecture): Prefecture(prefecture, self)
                             for prefecture in self.get_prefectures()}

        self.update_data()

    def get_prefectures(self):
        prefectures = set()
        for town in self._towns:
            prefectures.add(town.prefecture)

        return prefectures

    def update_data(self):

        for town in self._towns:
            if type(town.prefecture) == Prefecture:
                prefecture = self._prefectures[town.prefecture.name]
            else:
                prefecture = self._prefectures[town.prefecture]
            town.prefecture = prefecture
            prefecture.add_town(town)

            population = []

            for poprow in self._populations:

                unlinked = town.uid == poprow.town

                try:
                    linked = town.uid == poprow.town.uid
                except AttributeError:
                    linked = False

                if unlinked or linked:
                    population.append(poprow.population)
                    poprow.town = town

            town.population = population

    def update_datafile(self):

        self.write_populationfile()
        self.write_townfile()

    def write_populationfile(self):

        with open(self._populationdata_file, "w") as file:
            writer = csv.DictWriter(file, fieldnames=self._population_header)
            writer.writeheader()

            for population in sorted(self._populations, key=lambda x: x.uid):
                values = [population.uid, population.save, population.date,
                          -1, population.population]
                if type(population.town) == Town:
                    values[3] = population.town.uid
                else:
                    values[3] = population.town

                writer.writerow(dict(zip(self._population_header, values)))

    def write_townfile(self):

        with open(self._towndata_file, "w") as file:
            writer = csv.DictWriter(file, fieldnames=self._town_header)
            writer.writeheader()

            for town in sorted(self._towns, key=lambda x: x.uid):
                values = [town.uid, town.town, town.prefecture.name]
                if town.ward:
                    values.append(1)
                else:
                    values.append(0)
                if not town.city:
                    values.append("")
                else:
                    values.append(town.city)
                if not town.cur_population:
                    values.append("")
                else:
                    values.append(town.cur_population)
                if not town.start_save:
                    values.append("")
                else:
                    values.append(town.start_save)
                if not town.stop_save:
                    values.append("")
                else:
                    values.append(town.stop_save)
                if not town.planned:
                    values.append("")
                else:
                    values.append(town.planned)
                writer.writerow(dict(zip(self._town_header, values)))

    def population_row(self, import_row, save):
        prefectures = {item[0]: item[1] for item in sorted(
                       self._prefectures.items(), key=lambda x: x[1].name)}

        with open(self._populationdata_file) as file:
            reader = csv.DictReader(file)

            for i, row in enumerate(reader):
                pass

        values = [int(row["uid"]), int(save), import_row.pop("日付"), 0, 0]

        write_rows = []
        towns = {}

        for prefecture in prefectures.values():
            for town in sorted(prefecture.towns, key=lambda x: x.name):
                valid = town.start_save <= save and \
                    (not town.stop_save or save < town.stop_save)
                if valid:
                    towns[town.name] = town

        for name, population in import_row.items():
            if int(population) != 0:
                values[0] += 1
                values[3] = towns[name].uid
                values[4] = int(population)
                towns[name].population = int(population)
                write_rows.append(dict(zip(self._population_header, values)))

        with open(self._populationdata_file, "a") as file:
            writer = csv.DictWriter(file, fieldnames=self._population_header)

            for row in write_rows:
                writer.writerow(row)

    @property
    def folder(self):
        return self._folder

    @property
    def towns(self):
        return self._towns

    @property
    def active_towns(self):
        towns = []

        for town in self._towns:
            assert type(town) is Town

            try:
                if self.maxsave < town.stop_save and \
                        self.maxsave >= town.start_save:
                    towns.append(town)
            except TypeError:
                if self.maxsave >= town.start_save:
                    towns.append(town)

        return towns

    @property
    def populations(self):
        return self._populations

    @property
    def prefectures(self):
        return self._prefectures

    @property
    def dates(self):
        dates = sorted(list(self._dates))
        while "元" in dates[-1]:
            date = dates.pop()
            dates.insert(0, date)
        return dates

    @property
    def dates_np(self):
        dates = []
        for date in self.dates:
            year, dat = date.split("年")

            year = year.lstrip(self._period_name)

            if year == "元":
                year = self._start_period
            else:
                year = str(int(year) + int(self._start_period) - 1)

            dates.append("年".join([year, dat]))

        return dates

    @property
    def language(self):
        return self._language

    @property
    def mapname(self):
        return self._mapname.split("/")

    @property
    def subdiv(self):
        return self._subdiv.split("/")
