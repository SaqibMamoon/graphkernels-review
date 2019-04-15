#!/usr/bin/env python3
#
# create_kernel_matrices.py: Given a set of graphs, applies a number of
# graph kernels to them and stores the resulting kernel matrices.

import argparse
import logging
import os
import sys

import graphkernels.kernels as gk
import igraph as ig

from tqdm import tqdm


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('FILE', nargs='+', type=str, help='Input file(s)')
    parser.add_argument(
        '-f', '--force', action='store_true',
        help='If specified, overwrites data'
    )
    parser.add_argument(
        '-o', '--output',
        required=True,
        type=str,
        help='Output directory'
    )

    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format=None
    )

    # Check if the output directory already contains some files. If so,
    # do not run the script unless `--force` has been specified.
    if os.path.exists(args.output) and not args.force:
        logging.error('''
Output directory already exists. Refusing to continue unless `--force`
is specified.
        ''')

        sys.exit(-1)

    logging.info('Loading graphs...')

    graphs = [
        ig.read(filename, format='picklez') for filename in
            tqdm(args.FILE, desc='File')
    ]
