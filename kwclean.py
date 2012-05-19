#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: R.F. Smith <rsmith@xs4all.nl>
# Time-stamp: <2012-05-19 22:34:30 rsmith>
#
# To the extent possible under law, Roland Smith has waived all copyright and
# related or neighboring rights to dater. This work is published from the
# Netherlands. See http://creativecommons.org/publicdomain/zero/1.0/

import sys
import re

for line in sys.stdin:
    line = re.sub('\$Date.*\$', '$Date$', line)
    print re.sub('\$Revision.*\$', '$Revision$', line),
