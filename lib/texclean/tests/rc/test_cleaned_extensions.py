"""Tests for `texclean.rc.cleaned_extensions`."""
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
from tempfile import mkstemp

from nose.tools import assert_equal, raises

from texclean import cleaned_extensions


EXPECTED_DEFAULT = set(['aux', 'bbl', 'blg', 'dvi', 'log', 'lot', 'lof',
                        'nav', 'out', 'pdf', 'ps', 'snm', 'toc'])


def test_default_extensions():
    expected = EXPECTED_DEFAULT
    actual = set(cleaned_extensions())
    assert_equal(expected, actual)


def test_added_extensions():
    fd, filename = mkstemp()
    with open(filename, 'w') as rcfile:
        rcfile.write('xyz : delete\n123 : delete')
    expected = EXPECTED_DEFAULT.union(set(['xyz', '123']))
    actual = set(cleaned_extensions(rcfile=filename))
    os.remove(filename)
    assert_equal(expected, actual)


def test_removed_extensions():
    fd, filename = mkstemp()
    with open(filename, 'w') as rcfile:
        rcfile.write('toc : keep\npdf : keep')
    expected = EXPECTED_DEFAULT - set(['toc', 'pdf'])
    actual = set(cleaned_extensions(rcfile=filename))
    os.remove(filename)
    assert_equal(expected, actual)


def test_added_and_removed_extensions():
    fd, filename = mkstemp()
    with open(filename, 'w') as rcfile:
        rcfile.write('pdf : keep\nxyz : delete')
    expected = EXPECTED_DEFAULT.union(set(['xyz'])) - set(['pdf'])
    actual = set(cleaned_extensions(rcfile=filename))
    os.remove(filename)
    assert_equal(expected, actual)


@raises(ValueError)
def test_invalid_rc():
    fd, filename = mkstemp()
    with open(filename, 'w') as rcfile:
        rcfile.write('pdf : nodelete')
    try:
        deleted = cleaned_extensions(rcfile=filename)
    except:
        raise
    finally:
        os.remove(filename)
