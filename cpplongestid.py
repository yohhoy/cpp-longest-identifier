#!/usr/bin/env python3
"""
cpplongestid.py -- find longest identifier in C++ Standard

Copyright (c) 2018 yoh
"""
import os
import re

LENGTH_LIMIT = 25


def parse_subtex(basedir, texfile):
    identifers = set()
    with open(os.path.join(basedir, texfile), 'r') as f:
        in_itemdecl = False
        in_codeblock = False
        for line in f:
            if re.match(r'\\begin\{itemdecl\}', line):
                in_itemdecl = True
            elif re.match(r'\\end\{itemdecl\}', line):
                in_itemdecl = False
            elif re.match(r'\\begin\{codeblock\}', line):
                in_codeblock = True
            elif re.match(r'\\end\{codeblock\}', line):
                in_codeblock = False
            elif in_itemdecl or in_codeblock:
                m = re.findall(r'[_a-z][_a-z0-9]+', line)
                if m:
                    identifers.update(m)
    return [s for s in identifers if len(s) > LENGTH_LIMIT]


def parse_roottex(basedir, texfile):
    identifers = set()
    with open(os.path.join(basedir, texfile), 'r') as f:
        for line in f:
            m = re.match(r'\\include\{([a-z]+)\}', line)
            if not m:
                continue
            subtex = m.group(1) + '.tex'
            ids = parse_subtex(basedir, subtex)
            identifers.update(ids)
    identifers = sorted(list(identifers), key=lambda s: (-len(s), s))
    for name in identifers:
        print(name, len(name))


if __name__ == '__main__':
    parse_roottex('cppdraft/source', 'std.tex')
