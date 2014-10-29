#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Speedtest measurement archiver.

Usage:
    speedtest-archive [--iface=<name>] [--gatename=<name>] [--gatemac=<addr>]
    speedtest-archive -h | --help
    speedtest-archive --version

Options:
    -i <name>, --iface=<name>     Only run if on interface <name>
    -n <name>, --gatename=<name>  Only run if the default gateway name matches
                                  <name>
    -a <addr>, --gatemac=<addr>   Only run if the default gateway MAC address
                                  matches <addr>

<https://github.com/jonasmalacofilho/speedtest-archive>
Copyright 2014 Jonas Malaco Filho.
Licensed under the Modified BSD (3-clause) License.
"""

from __future__ import print_function
from datetime import datetime
from docopt import docopt
from minifixed import reader as fixedreader
from subprocess import Popen, PIPE
import json
import sys


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


version = "0.1.2"


if __name__ == "__main__":

    args = docopt(__doc__)
    if args["--help"] or args["-h"]:
        print(__doc__)
        sys.exit(0)
    if args["--version"]:
        print(version)
        sys.exit(0)

    # get infos
    info = get_gateway_info()
    if args["--iface"] and args["--iface"] != info["interface"]:
        sys.exit(21)
    if args["--gatename"] and args["--gatename"] != info["gateway_name"]:
        sys.exit(22)
    if args["--gatemac"] and args["--gatemac"] != info["gateway_mac"]:
        sys.exit(23)

    # collect data
    time = datetime.now().isoformat()
    res = speedtest()

    # output
    out = [
        time,
        info["interface"], info["gateway_name"], info["gateway_mac"],
        str(res["ping"]), str(res["download"]), str(res["upload"]),
        str(res["server"]), res["share"]
    ]
    print("\t".join(out))

