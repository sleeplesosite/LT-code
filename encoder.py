#!/usr/bin/env python3
import argparse
import sys
import time
from functools import reduce
from operator import xor
import pdb
from struct import pack

import lt_sampler

# Block file byte contents into blocksize chunks, padding last one if necessary
# FIXME: make this cross-platform - have to check byte order of file right?
def get_blocks(f, blocksize):
    f_bytes = f.read()
    blocks = [int.from_bytes(f_bytes[i:i+blocksize].ljust(blocksize, b'0'), 'big') for i in range(0, len(f_bytes), blocksize)]
    return len(f_bytes), blocks

# Generator of blocks
def lt_encoder(fn, blocksize, seed, c, delta):

    # get file blocks
    with open(fn, 'rb') as f:
        filesize, blocks = get_blocks(f, blocksize)

    K = len(blocks)
    prng = lt_sampler.PRNG(params=(K, delta, c))
    prng.set_seed(seed)

    # block generation loop
    while True:
        blockseed, d, ix_samples = prng.get_src_blocks()
        block_data = 0
        for ix in ix_samples:
            block_data ^= blocks[ix]
        yield (filesize, blocksize, blockseed, int.to_bytes(block_data, blocksize, 'big'))

def write_out(block):
    sys.stdout.buffer.write(pack('!IIIs', *block))

# Run that ish
def run(fn, blocksize, seed, c, delta):
    encoder = lt_encoder(fn, blocksize, seed, c, delta)
    for block in encoder:
        sys.stdout.buffer.write(pack('!III%ss'%blocksize, *block))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file', help='the source file to encode')
    parser.add_argument('blocksize', metavar='block-size', 
                                     type=int, 
                                     help='the size of each encoded block, in bytes')
    parser.add_argument('seed', type=int,
                                nargs="?",
                                default=2067261,
                                help='the initial seed for the random number generator')
    parser.add_argument('c', type=float,
                             nargs="?",
                             default=lt_sampler.PRNG_C,
                             help='degree sampling distribution tuning parameter')
    parser.add_argument('delta', type=float,
                                 nargs="?",
                                 default=lt_sampler.PRNG_DELTA,
                                 help='degree sampling distribution tuning parameter')
    args = parser.parse_args()

    run(args.file, args.blocksize, args.seed, args.c, args.delta)
