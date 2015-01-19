#!/usr/bin/python

# Copyright (C) 2015  Allen Li
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
binasphere.py
=============

Hymnnos Binasphere tool.

Short script to assist in Binasphere construction (or other text weaving needs).

    $ echo 'I see
    Do you see me?' > tmp
    $ python binasphere.py join 0,1,1 <tmp
    I Do you see see me?
    $ echo 'I Do you see see me?' | python binasphere.py split 0,1,1
    I see
    Do you see me?

You can also import and use the module.

    >>> import binasphere
    >>> binasphere.join([0, 1, 1], ['I see', 'Do you see me?'])
    'I Do you see see me?'
    >>> binasphere.split([0, 1, 1], 'I Do you see see me?')
    ['I see', 'Do you see me?']

"""

import argparse
from collections import deque
import logging
import sys


def _parse_pattern(pattern):
    """Parse Binasphere pattern."""
    return [int(x) for x in pattern.split(',')]


def split(pattern, lyrics):
    """Split Binasphere lines.

    Args:
        pattern: List of integers indicating join pattern.
        lyrics: String to split.

    >>> split([0, 1, 1], 'a b c d e f')
    ['a d', 'b c e f']

    """
    lyrics = lyrics.split()
    num_lines = max(pattern) + 1
    result = [list() for i in range(num_lines)]
    i = 0
    for word in lyrics:
        val = pattern[i]
        result[val].append(word)
        i += 1
        i %= len(pattern)
    if i != 0:
        logging.warning('Pattern is not fully matched, ended on %d', i)
    return [' '.join(line) for line in result]


def join(pattern, lyrics):
    """Join together Binasphere lines.

    Args:
        pattern: List of integers indicating join pattern.
        lyrics: List of strings, choruses to join.

    >>> join([0, 1, 1], ['a b', 'c d e f'])
    'a c d b e f'

    """
    lyrics = [deque(line.split()) for line in lyrics]
    result = []
    while True:
        for val in pattern:
            cur_line = lyrics[val]
            try:
                word = cur_line.popleft()
            except IndexError:
                logging.error('Line %d is missing words.', val)
                sys.exit(1)
            result.append(word)
        if not any(lyrics):  # if all lines in result are empty
            break
    return ' '.join(result)


def _split_cmd(args):
    """Split command."""
    pattern = _parse_pattern(args.pattern)
    lyrics = sys.stdin.read()
    result = split(pattern, lyrics)
    print('\n'.join(result))


def _join_cmd(args):
    """Join command."""
    pattern = _parse_pattern(args.pattern)
    lyrics = []
    for line in sys.stdin:
        lyrics.append(line)
    result = join(pattern, lyrics)
    print(result)


def main():

    """Main function."""

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(title='Commands')

    tmp_parser = subparsers.add_parser('split')
    tmp_parser.add_argument('pattern')
    tmp_parser.set_defaults(func=_split_cmd)

    tmp_parser = subparsers.add_parser('join')
    tmp_parser.add_argument('pattern')
    tmp_parser.set_defaults(func=_join_cmd)

    args = parser.parse_args()
    try:
        func = args.func
    except AttributeError:
        parser.print_help()
    else:
        func(args)


if __name__ == '__main__':
    main()
