#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2014 Jonas Malaco Filho
# Licensed under the Modified BSD (3-clause) License

from __future__ import print_function
from datetime import datetime
from minifixed import reader as fixedreader
from subprocess import Popen, PIPE
import json


def get_routing_table():
    proc = Popen(["/sbin/route"], stdout=PIPE)
    if proc.wait() != 0:
        raise Exception(
            "'/sbin/route' exited with non zero status: {}"
            .format(proc.returncode))
    proc.stdout.readline()  # skip the 1st line: Kernel IP...
    return list(fixedreader(proc.stdout))


def get_arp_table():
    proc = Popen(["/usr/sbin/arp"], stdout=PIPE)
    if proc.wait() != 0:
        raise Exception(
            "'/usr/sbin/arp' exited with non zero status: {}"
            .format(proc.returncode))
    return list(fixedreader(proc.stdout))


def get_gateway_info():
    routes = get_routing_table()
    arps = get_arp_table()

    gateway = filter(lambda x: x["Destination"] == "default", routes)[0]
    gateway_arp = filter(lambda x: x["Address"] == gateway["Gateway"], arps)[0]

    return {"gateway_name": gateway["Gateway"],
            "gateway_mac": gateway_arp["HWaddress"],
            "interface": gateway["Iface"]}


def speedtest():
    proc = Popen(["/usr/local/bin/speedtest", "--share", "--json"], stdout=PIPE)
    if proc.wait() != 0:
        raise Exception(
            "'/usr/local/bin/speedtest' exited with non zero status: {}"
            .format(proc.returncode))
    return json.loads(proc.stdout.read())


if __name__ == "__main__":
    time = datetime.now().isoformat()
    info = get_gateway_info()
    res = speedtest()

    out = [
        time,
        info["interface"], info["gateway_name"], info["gateway_mac"],
        str(res["ping"]), str(res["download"]), str(res["upload"]),
        str(res["server"]), res["share"]
    ]

    print("\t".join(out))
