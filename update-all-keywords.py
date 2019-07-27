#!/usr/bin/env python3
# file: update-all-keywords.py
# vim:fileencoding=utf-8:fdm=marker:ft=python
#
# Copyright © 2013-2015 R.F. Smith <rsmith@xs4all.nl>.
# SPDX-License-Identifier: MIT
# Created: 2013-07-17T18:06:53+02:00
# Last modified: 2019-07-27T20:56:24+0200
"""Remove and check out all files under git's control that contain keywords in
the current working directory."""

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
        logging.error('No .git directory found!')
        sys.exit(1)
    # Get all files that are controlled by git.
    files = git_ls_files()
    # Remove those that aren't checked in
    mod = git_not_checkedin()
    if mod:
        files = [f for f in files if f not in mod]
    if not files:
        print('{}: Only uncommitted changes, nothing to do.'.format(args[0]))
        sys.exit(0)
    files.sort()
    # Find files that have keywords in them
    kwfn = keywordfiles(files)
    if kwfn:
        print('{}: Updating all files.'.format(args[0]))
        for fn in kwfn:
            os.remove(fn)
        sargs = ['git', 'checkout', '-f'] + kwfn
        sp.run(sargs, stdout=sp.DEVNULL, stderr=sp.DEVNULL)
    else:
        print('{}: Nothing to update.'.format(args[0]))


def git_ls_files():
    """Find ordinary files that are controlled by git.

    Returns:
        A list of files
    """
    args = ['git', 'ls-files']
    cp = sp.run(args, text=True, stdout=sp.PIPE, stderr=sp.DEVNULL)
    return cp.stdout.splitlines()


def git_not_checkedin():
    """Find files that are modified but are not checked in.

    Returns:
        A list of modified files that are not checked in.
    """
    cp = sp.run(['git', 'status', '-s'], text=True, stdout=sp.PIPE, stderr=sp.DEVNULL)
    return [l.split()[-1] for l in cp.stdout.splitlines()]


def keywordfiles(fns):
    """Filter those files that have keywords in them

    Arguments:
        fns: A list of filenames.

    Returns:
        A list for filenames for files that contain keywords.
    """
    # These lines are encoded otherwise they would be mangled if this file
    # is checked in!
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
