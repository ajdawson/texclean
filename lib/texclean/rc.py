"""Handle rc file and default file extensions."""
# Copyright (c) 2013 Andrew Dawson
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
from __future__ import absolute_import

import os


#: Files with the following extensions will be deleted by default.
DEFAULT_EXTENSIONS = ('aux', 'bbl', 'blg', 'dvi', 'log', 'lot', 'lof', 'nav',
                      'out', 'pdf', 'ps', 'snm', 'toc',)


def _strip_comments(line, comment_character='#'):
    """Remove comments from lines."""
    pos = line.find(comment_character)
    if pos < 0:
        return line
    return line[:pos]


def _parse_rc_line(line):
    try:
        config, value = [keyvalue.strip() for keyvalue in line.split(':')]
    except (ValueError, TypeError):
        raise ValueError('invalid configuration line: {}'.format(line))
    if value.lower() == 'delete':
        value = True
    elif value.lower() == 'keep':
        value = False
    else:
        raise ValueError('invalid configuration value: {}, values must '
                         'be either "delete" or "keep"'.format(value))
    return config, value


def _rc_extensions(rcfile):
    with open(rcfile, 'r') as f:
        rclines = filter(lambda l: l.strip(),
                         map(_strip_comments, f.readlines()))
    rcdict = {}
    for line in rclines:
        config, value = _parse_rc_line(line)
        rcdict[config] = value
    return rcdict


def cleaned_extensions(rcfile=None):
    extensions = {k: True for k in DEFAULT_EXTENSIONS}
    if rcfile is not None:
        rc = _rc_extensions(rcfile)
        extensions.update(rc)
    return [ext for ext in extensions if extensions[ext]]
