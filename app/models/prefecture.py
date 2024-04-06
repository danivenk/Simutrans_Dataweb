#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
version: python 3+
prefecture.py defines the Prefecture model used for this app
Dani van Enk
"""
# import os
# import csv

from .town import Town


class Prefecture:
    i = 0

    def __init__(self, name, Data_Object):
        self._uid = self.i
        self._name = name
        self._towns = []

        self.i += 1

        self.data = Data_Object

    def add_town(self, town):
        assert type(town) == Town

        self._towns.append(town)

    @property
    def name(self):
        return self._name

    @property
    def towns(self):
        return self._towns

    @property
    def population(self):
        population = [0 for _ in range(self.data.maxsave)]
        for town in self._towns:
            try:
                if self.data.maxsave < town.stop_save and \
                        self.data.maxsave >= town.start_save:
                    for i, value in enumerate(town.population):
                        population[i] += value
            except TypeError:
                if self.data.maxsave >= town.start_save:
                    for i, value in enumerate(town.population):
                        population[i] += value

        return population

    @property
    def cur_population(self):
        try:
            return self.population[-1]
        except IndexError:
            return None

    def __repr__(self):
        return self._name
