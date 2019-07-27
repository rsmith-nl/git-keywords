#!/usr/bin/env python3
# file: update-modified-keywords.py
# vim:fileencoding=utf-8:fdm=marker:ft=python
#
# Copyright © 2013-2015 R.F. Smith <rsmith@xs4all.nl>.
# SPDX-License-Identifier: MIT
# Created: 2013-07-17T18:58:42+02:00
# Last modified: 2019-07-27T21:01:32+0200
"""Remove and check out those files that that contain keywords and have
changed since in the last commit in the current working directory."""

from base64 import b64decode
import mmap
import logging
import os
import subprocess as sp
import sys


def main(args):
    """Main program.

    Arguments:
        args: command line arguments
    """
    logging.basicConfig(level='INFO', format='%(levelname)s: %(message)s')
    # Check if git is available.
    try:
        sp.run(['git'], stdout=sp.DEVNULL, stderr=sp.DEVNULL)
        logging.info('found “git”')
    except FileNotFoundError:
        logging.error('the program “git” cannot be found')
        sys.exit(1)
    # Check if .git exists
    if not os.access('.git', os.F_OK):
        print('No .git directory found!')
        sys.exit(1)
    print('{}: Updating modified files.'.format(args[0]))
    # Get modified files
    files = modifiedfiles()
    if not files:
        print('{}: No modified files.'.format(args[0]))
        sys.exit(0)
    files.sort()
    # Find files that have keywords in them
    kwfn = keywordfiles(files)
    if not kwfn:
        print('{}: No keyword files modified.'.format(args[0]))
        sys.exit(0)
    for fn in kwfn:
        os.remove(fn)
    sargs = ['git', 'checkout', '-f'] + kwfn
    sp.call(sargs)


def modifiedfiles():
    """Find files that have been modified in the last commit.

    Returns:
        A list of filenames.
    """
    fnl = []
    try:
        args = ['git', 'diff-tree', 'HEAD~1', 'HEAD', '--name-only', '-r',
                '--diff-filter=ACMRT']
        cp = sp.check_output(
            args, stdout=sp.PIPE, stderr=sp.DEVNULL, text=True, check=True
        )
        fnl = cp.stdout.splitlines()
        # Deal with unmodified repositories
        if len(fnl) == 1 and fnl[0] == 'clean':
            return []
    except sp.CalledProcessError:
        if cp.returncode == 128:  # new repository
            args = ['git', 'ls-files']
            cp = sp.run(args, stdout=sp.PIPE, stderr=sp.DEVNULL, text=True)
            fnl = cp.stdout.splitlines()
    # Only return regular files.
    fnl = [i for i in fnl if os.path.isfile(i)]
    return fnl


def keywordfiles(fns):
    """Filter those files that have keywords in them

    Arguments:
        fns: A list of filenames.

    Returns:
        A list for filenames for files that contain keywords.
    """
    # These lines are encoded otherwise they would be mangled if this file
    # is checked in my git repo!
    datekw = b64decode('JERhdGU=')
    revkw = b64decode('JFJldmlzaW9u')
    rv = []
    for fn in fns:
        with open(fn, 'rb') as f:
            try:
                mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
                if mm.find(datekw) > -1 or mm.find(revkw) > -1:
                    rv.append(fn)
                mm.close()
            except ValueError:
                pass
    return rv


if __name__ == '__main__':
    main(sys.argv)
