# -*- coding: utf-8 -*-

import argparse
import os
import sys

from datetime import datetime

from pixget import PixGet


def main():
    """ Main script that handles parsing the arguments. """
    now = datetime.now()

    parser = argparse.ArgumentParser(description='Get some pix by file input.')
    parser.add_argument(
        '-i',
        '--infile',
        help='Path to input file  (default: %(default)s)',
        default='input.txt'
    )
    default_output = now.strftime('%Y-%m-%d-%H-%M')
    parser.add_argument(
        '-o',
        '--output',
        help='Output directory name (defaults to current ' \
             'timestamp: %(default)s, will be added if default, ' \
             'otherwise it must exist! Existing content will be ' \
             'overwritten)',
        default=default_output
    )
    parsed = parser.parse_args()

    ## check the input file
    if not os.path.exists(parsed.infile):
        print '\nWARNING: Input file at "%s" not found\n' % (parsed.infile)
        parser.print_help()
        sys.exit(1)

    ## check the output directory: if it is the default, add it
    ## otherwise check existence
    if parsed.output == default_output:
        if not os.path.exists(parsed.output):
            os.mkdir(parsed.output)
    else:
        if not os.path.exists(parsed.output):
            print 'Output directory does not exist at "%s"' % (parsed.output)
            sys.exit(1)

    pixget = PixGet(parsed.infile, parsed.output)
    pixget.run()
