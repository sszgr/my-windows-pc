#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
wt.py
~~~~~~~~
    // make directories
"""

import sys
import yaml
import argparse
from pathlib import Path

VERSION = 1.0

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file', required=True, help="configuration file")
parser.add_argument('--mkdir', default=None, help="make directories")
parser.add_argument('-t', '--tree', action='store_true', help="list contents of configuration in a tree-like format")
parser.add_argument('-v', '--version', action='version', version=str(VERSION))


def create(childs, bp: Path):
    while childs:
        item = childs.popitem()
        bp.joinpath(item[0]).mkdir(exist_ok=True, parents=True)
        if item[1] and 'childs' in item[1]:
            create(item[1]['childs'], bp.joinpath(item[0]))


def display(childs, prefix=''):

    item = None

    while childs:
        if not item:
            item = childs.popitem()
            continue

        # middle
        print(prefix + "├── " + item[0])
        if item[1] and 'childs' in item[1]:
            display(item[1]['childs'], prefix + "│   ")

        item = childs.popitem()

    if item:
        print(prefix + "└── " + item[0])
        if item[1] and 'childs' in item[1]:
            display(item[1]['childs'], prefix + "    ")


args = parser.parse_args()

if not Path(args.file).is_file():
    print("No such file", file=sys.stderr)
    exit(1)

with open(args.file) as fp:
    config_dict = yaml.load(fp, Loader=yaml.FullLoader)

if VERSION < config_dict['version']:
    print("unsupported version")
    exit(1)

if args.mkdir:
    create(config_dict['directories'], Path(args.mkdir))

elif args.tree:
    print(args.file)
    display(config_dict['directories'])
