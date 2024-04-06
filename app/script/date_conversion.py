#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import dotenv as dot
import os
from datetime import datetime


def convert(data, date):
    date = datetime.strptime(date, "%Y/%m/%d")
    md_date = date.strftime("%m月%d日")
    y_date = int(date.year)

    dot.load_dotenv(os.path.join(data.folder, ".env"))
    start_p = os.getenv("start_period")
    name = os.getenv("name_period")

    if not start_p or not name:
        return f"{y_date}年{md_date}"

    p_date = y_date - int(start_p) + 1

    if p_date == 1:
        return f"{name}元年{md_date}"
    else:
        return f"{name}{p_date}年{md_date}"
