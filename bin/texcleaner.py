#!/usr/bin/env python
"""Delete files resulting from LaTeX compilations."""
# Copyright (c) 2013-2016 Andrew Dawson
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
from __future__ import print_function
import os
import sys
from argparse import ArgumentParser, RawDescriptionHelpFormatter

from texclean import clean_document, cleaned_extensions


def _summarize(docname, deleted):
    """Summarize which files were deleted for a given document."""
    print(docname)
    print('-' * len(docname))
    for f in deleted:
        print(f)
    print('{} files deleted'.format(len(deleted)))
    print()


def main(argv=None):
    if argv is None:
        argv = sys.argv
    # Set-up parsing command line arguments.
    ap = ArgumentParser(prog=os.path.basename(argv[0]),
                        description=__doc__,
                        formatter_class=RawDescriptionHelpFormatter)
    ap.add_argument('-n', '--dry-run', action='store_true',
                    help='print what would be done without doing it')
    ap.add_argument('-d', '--delete', metavar='ext[,ext]',
                    default='', type=str,
                    help='file extension(s) to be deleted '
                         'in addition to the defaults')
    ap.add_argument('-k', '--keep', metavar='ext[,ext]',
                    default='', type=str,
                    help='file extensions to be kept')
    ap.add_argument('-f', '--rcfile',
                    default=os.path.expanduser('~/.texcleanerrc'), type=str,
                    help='an alternate rc file to be used '
                         'instead of ~/.texcleanerrc')
    ap.add_argument('-s', '--summarize', action='store_true',
                    help='print a summary for each document')
    ap.add_argument('docname', nargs='+',
                    help='delete compilation files for the named document')
    args = ap.parse_args(argv[1:])

    try:
        delete = args.delete.split(',')
        keep = args.keep.split(',')
        if not os.path.exists(args.rcfile):
            rcfile = None
        else:
            rcfile = args.rcfile
        exts = cleaned_extensions(rcfile)
        exts = set([ext for ext in cleaned_extensions(rcfile) + delete
                    if ext not in keep])
        for docname in args.docname:
            deleted = clean_document(docname, exts, dry_run=args.dry_run)
            if args.summarize:
                _summarize(docname, deleted)
        return 0
    except ValueError as err:
        print('error: {!s}'.format(e), file=sys.stderr)
        print('  use -h or --help for help', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
