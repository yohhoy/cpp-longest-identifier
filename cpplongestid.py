#!/usr/bin/env python3
"""
cpplongestid.py -- find longest identifier in C++ Standard

Copyright (c) 2018,2020 yoh
"""
import os
import re

LENGTH_LIMIT = 30
USE_EXAMPLE = True


def parse_subtex(basedir, texfile):
    identifers = set()
    blk = {k[0]: False for k in ['itemdecl', 'codeblock', 'example']}
    pattern = re.compile(r'\\(begin|end)\{(itemdecl|codeblock|example)\}')
    with open(os.path.join(basedir, texfile), 'r') as f:
        for line in f:
            m = pattern.match(line)
            if m:
                key = m.groups()[1][0]  # use first char as key
                blk[key] = (m.groups()[0] == 'begin')
            elif (blk['i'] or blk['c']) and (not blk['e'] or USE_EXAMPLE):
                identifers.update(re.findall(r'[_a-z][_a-z0-9]+', line))
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
