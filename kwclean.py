#!/usr/bin/env python3
# file: kwclean.py
# vim:fileencoding=utf-8:ft=python
#
# Copyright © 2012-2014 R.F. Smith <rsmith@xs4all.nl>.
# SPDX-License-Identifier: MIT
# Created: 2012-05-19T22:35:54+02:00
# Last modified: 2018-04-17T18:53:52+0200
"""Remove the Date and Revision keyword contents from the standard input."""

import io
import re
import sys

if __name__ == '__main__':
    dre = re.compile(''.join([r'\$', r'Date.*?\$']))
    drep = ''.join(['$', 'Date', '$'])
    rre = re.compile(''.join([r'\$', r'Revision.*?\$']))
    rrep = ''.join(['$', 'Revision', '$'])
    input_stream = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
    for line in input_stream:
        line = dre.sub(drep, line)
        print(rre.sub(rrep, line), end="")
