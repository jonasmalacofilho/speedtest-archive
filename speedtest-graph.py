#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2014 Jonas Malaco Filho
# Licensed under the Modified BSD (3-clause) License

from __future__ import print_function
from sys import stdin, stdout
import matplotlib.pyplot as plt
import dateutil.parser


def parse_date(text):
    date = dateutil.parser.parse(text)
    # return int(date.strftime("%s"))
    return date


def parse_ping(text):
    return float(text)


def parse_speed(text):
    return float(text)/1000/1000*8


def parse_record(text):
    s = text.split("\t")
    return (parse_date(s[0]), parse_ping(s[4]), parse_speed(s[5]),
            parse_speed(s[6]))


time, ping, down, up = zip(*map(parse_record, list(stdin)))

plt.rc("lines", linewidth=.2)
plt.rc("font", family="sans-serif", size=6)
grid = True
plt.figure(figsize=(16, 9))

plt.subplot2grid((5, 1), (0, 0), rowspan=2)
plt.plot(time, down, color="blue")
plt.ylabel("Download (Mb/s)")
plt.xticks(plt.xticks()[0], [])
plt.grid(grid)

plt.subplot2grid((5, 1), (2, 0), rowspan=2)
plt.plot(time, up, color="green")
plt.ylabel("Upload (Mb/s)")
plt.xticks(plt.xticks()[0], [])
plt.grid(grid)

plt.subplot2grid((5, 1), (4, 0))
plt.plot(time, ping, color="red")
plt.ylabel("Ping (ms)")
plt.xticks(plt.xticks()[0], [])
plt.grid(grid)

plt.tight_layout(pad=5)

plt.savefig(stdout, format="svg")
