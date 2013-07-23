#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: R.F. Smith <rsmith@xs4all.nl>
# $Date$
#
# To the extent possible under law, Roland Smith has waived all copyright and
# related or neighboring rights to kwset.py. This work is published from
# the Netherlands. See http://creativecommons.org/publicdomain/zero/1.0/

"""Fill the Date and Revision keywords from the latest git commit and tag and
   subtitutes them in the standard input."""

import os
import sys
import subprocess
import re


def gitdate():
    """Get the date from the latest commit in ISO8601 format.
    """
    args = ['git', 'log',  '-1', '--date=iso']
    dline = [l for l in subprocess.check_output(args).splitlines() 
             if l.startswith('Date')]
    try:
        dat = dline[0][5:].strip()
        return ''.join(['$', 'Date: ', dat, ' $'])
    except IndexError:
        raise ValueError('Date not found in git output')


def gitrev():
    """Get the latest tag and use it as the revision number. This presumes the
    habit of using numerical tags. Use the short hash if no tag available.
    """
    args = ['git', 'describe',  '--tags', '--always']
    try:
        with open(os.devnull, 'w') as bb:
            r = subprocess.check_output(args, stderr=bb)[:-1]
    except subprocess.CalledProcessError:
        return ''.join(['$', 'Revision', '$'])
    return ''.join(['$', 'Revision: ', r, ' $'])


def main():
    """Main program.
    """
    dre = re.compile(''.join([r'\$', r'Date:?\$']))
    rre = re.compile(''.join([r'\$', r'Revision:?\$']))
    currp = os.getcwd()
    if not os.path.exists(currp+'/.git'):
        print >> sys.stderr, 'This directory is not controlled by git!'
        sys.exit(1)
    date = gitdate()
    rev = gitrev()
    for line in sys.stdin:
        line = dre.sub(date, line)
        print rre.sub(rev, line),


## This is the main program ##
if __name__ == '__main__':
    main()
