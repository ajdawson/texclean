"""Tests for `texclean.cleaner.clean_document`."""
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

from mock import Mock, patch

from texclean import clean_document


def test_default():
    # make sure a call to delete is made for every file we expect
    # and no more, and that this matches the return value
    document_name = './test_document.tex'
    extensions = ('aux', 'pdf')
    base_name, _ = os.path.splitext(document_name)
    expected_deleted = ['{}.{}'.format(base_name, extension)
                        for extension in extensions]
    with patch('os.path.exists', new=Mock(return_value=True)):
        with patch('os.remove') as patched_os_remove:
            deleted = clean_document(document_name, extensions)
            # os.remove should be called once for each file deleted
            assert patched_os_remove.call_count == len(expected_deleted)
            for filename in expected_deleted:
                # os.remove should be called for every file deleted
                patched_os_remove.assert_any_call(filename)
    # the list of deleted files should match the expected list
    assert sorted(deleted) == sorted(expected_deleted)


def test_dry_run():
    document_name = './test_document.tex'
    extensions = ('aux', 'pdf')
    base_name, _ = os.path.splitext(document_name)
    expected_deleted = ['{}.{}'.format(base_name, extension)
                        for extension in extensions]
    with patch('os.path.exists', new=Mock(return_value=True)):
        with patch('os.remove') as patched_os_remove:
            deleted = clean_document(document_name, extensions, dry_run=True)
            # os.remove should not be called in a dry run
            assert not patched_os_remove.called
    # the list of deleted files should still be correct though
    assert sorted(deleted) == sorted(expected_deleted)
