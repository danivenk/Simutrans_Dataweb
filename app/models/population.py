#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
version: python 3+
population.py defines the population model used for this app
Dani van Enk
"""

from .town import Town


class Population:

    def __init__(self, data, Data_object):

        assert type(data) == list and len(data) == 5

        for i, item in enumerate(data):
            if item == "":
                data[i] = None

        self.uid = int(data[0])
        self._save = int(data[1])
        self._date = data[2]
        if type(data[3]) == Town:
            self._town = data[3]
        else:
            self._town = int(data[3])
        self._population = int(data[4])

        self.data = Data_object

    @property
    def save(self):
        return self._save

    @property
    def date(self):
        return self._date

    @property
    def town(self):
        return self._town

    @town.setter
    def town(self, val):
        self._town = val

    @property
    def population(self):
        try:
            return self._population
        except AttributeError:
            return None

    @population.setter
    def population(self, val):
        self._population = val

    def __repr__(self):
        return f"{self._save} - {self.town}:{self._date} " \
            f"- {self._population}"
