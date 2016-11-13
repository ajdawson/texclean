"""Remove files resulting from LaTeX compilations."""
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


def _delete(filepath, dry_run=False):
    if dry_run:
        return
    os.remove(filepath)


def clean_document(document_name, clean_extensions, dry_run=False):
    path, name = os.path.split(document_name)
    if not path:
        path = '.'
    plain_name = os.path.splitext(name)[0]
    deleted_files = []
    for ext in clean_extensions:
        filepath = os.path.join(path, '{}.{}'.format(plain_name, ext))
        if os.path.exists(filepath):
            _delete(filepath, dry_run)
            deleted_files.append(filepath)
    return deleted_files
