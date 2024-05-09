#!/usr/bin/env python3
# file: kwset.py
# vim:fileencoding=utf-8:ft=python
#
# Copyright © 2013-2015 R.F. Smith <rsmith@xs4all.nl>.
# SPDX-License-Identifier: MIT
# Created: 2013-07-23T16:14:31+02:00
# Last modified: 2018-04-17T18:54:08+0200

"""Fill the Date and Revision keywords from the latest git commit and tag and
   subtitutes them in the standard input."""

import io
import os
import re
import subprocess
import sys


def main():
    """Main program.
    """
    dre = re.compile(''.join([r'\$', r'Date:?\$']))
    rre = re.compile(''.join([r'\$', r'Revision:?\$']))
    currp = os.getcwd()
    if not os.path.exists(currp + '/.git'):
        print >> sys.stderr, 'This directory is not controlled by git!'
        sys.exit(1)
    date = gitdate()
    rev = gitrev()
    input_stream = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
    for line in input_stream:
        line = dre.sub(date, line)
        print(rre.sub(rev, line), end="")


def gitdate():
    """Get the date from the latest commit in ISO8601 format.
    """
    args = ['git', 'log', '-1', '--date=iso']
    outdata = subprocess.check_output(args, universal_newlines=True)
    outlines = outdata.splitlines()
    dline = [l for l in outlines if l.startswith('Date')]
    try:
        dat = dline[0][5:].strip()
        return ''.join(['$', 'Date: ', dat, ' $'])
    except IndexError:
        raise ValueError('Date not found in git output')


def gitrev():
    """Get the latest tag and use it as the revision number. This presumes the
    habit of using numerical tags. Use the short hash if no tag available.
    """
    args = ['git', 'describe', '--tags', '--always']
    try:
        r = subprocess.check_output(args,
                                    stderr=subprocess.DEVNULL,
                                    universal_newlines=True)[:-1]
    except subprocess.CalledProcessError:
        return ''.join(['$', 'Revision', '$'])
    return ''.join(['$', 'Revision: ', r, ' $'])


if __name__ == '__main__':
    main()
