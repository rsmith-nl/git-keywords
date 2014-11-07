#!/usr/bin/env python
# vim:fileencoding=utf-8:ft=python
#
# Author: R.F. Smith <rsmith@xs4all.nl>
# $Date$
#
# To the extent possible under law, Roland Smith has waived all copyright and
# related or neighboring rights to kwclean.py. This work is published from the
# Netherlands. See http://creativecommons.org/publicdomain/zero/1.0/

"""Remove the Date and Revision keyword contents from the standard input."""

import sys
import re

if __name__ == '__main__':
    dre = re.compile(''.join([r'\$', r'Date.*\$']))
    drep = ''.join(['$', 'Date', '$'])
    rre = re.compile(''.join([r'\$', r'Revision.*\$']))
    rrep = ''.join(['$', 'Revision', '$'])
    for line in sys.stdin:
        line = dre.sub(drep, line)
        print rre.sub(rrep, line),
