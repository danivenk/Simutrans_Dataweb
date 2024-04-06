#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
version: python 3+
town.py defines the town model used for this app
Dani van Enk
"""
# import os
# import csv


class Town:
    def __init__(self, data, Data_object):

        assert type(data) == list and len(data) == 9

        for i, item in enumerate(data):
            if item == "":
                data[i] = None

        self.uid = int(data[0])
        self._town = data[1]
        self._prefecture = data[2]
        if int(data[3]) != 1:
            self._ward = False
        else:
            self._ward = True
        if data[4]:
            self._city = data[4]
        if data[5]:
            self._population = int(data[5])
        if data[6]:
            self._start_save = int(data[6])
        if data[7]:
            self._stop_save = int(data[7])
        if data[8]:
            self._planned_population = int(data[8])

        self.data = Data_object

    @property
    def name(self):
        if self._ward and self.data._language == "JP":
            return f"{self._city}｜{self._town}区"
        elif self._ward:
            return f"{self._city} {self._town}"
        return f"{self._town}"

    @property
    def town(self):
        return self._town

    @property
    def ward(self):
        if not self._ward:
            return None
        return self._town

    @property
    def city(self):
        try:
            return self._city
        except AttributeError:
            return None

    @property
    def prefecture(self):
        return self._prefecture

    @prefecture.setter
    def prefecture(self, val):
        self._prefecture = val

    @property
    def start_save(self):
        try:
            return self._start_save
        except AttributeError:
            return None

    @property
    def stop_save(self):
        try:
            return self._stop_save
        except AttributeError:
            return None

    @property
    def population(self):
        try:
            return self._population
        except AttributeError:
            return None

    @population.setter
    def population(self, val):

        if len(val) != self.data.maxsave:
            for _ in range(1, self.start_save):
                val.insert(0, 0)

            if self.stop_save:
                for _ in range(self.stop_save, self.data.maxsave + 1):
                    val.append(0)

        self._population = val

    @property
    def cur_population(self):
        try:
            return self._population[-1]
        except IndexError:
            return None

    @property
    def planned(self):
        try:
            return self._planned_population
        except AttributeError:
            return None

    @planned.setter
    def planned(self, val):
        try:
            len(val)
        except TypeError:
            self._planned_population = val

    @property
    def growth_stopped(self):
        growth_check = self._population[-3:-1]
        change = 0
        for i in range(len(growth_check) - 1):
            change += abs(growth_check[i + 1] - growth_check[i])

            if change != 0:
                return False

        return True

    def __repr__(self):
        if self._ward and self.data._language == "JP":
            return f"{self._prefecture}｜{self._town}区"
        elif self.data._language == "JP":
            return f"{self._prefecture}｜{self._town}"
        return f"{self._prefecture}, {self.town}"
