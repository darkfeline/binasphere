#!/usr/bin/python

"""
Hymnnos Binasphere tool

Join
----

Input: comma separated pattern values, starting from 0

Input: Lyrics.  Lines separated with newlines, words separated with spaces.

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
    #parser.set_defaults(func=lambda x: parser.print_help())
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
