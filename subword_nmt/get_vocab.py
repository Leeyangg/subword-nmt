#! /usr/bin/env python
from __future__ import print_function
import sys
from collections import Counter

# hack for python2/3 compatibility
from io import open
argparse.open = open

def create_parser(subparsers=None):

    if subparsers:
        parser = subparsers.add_parser('get-vocab',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            description="Generates vocabulary")
    else:
        parser = subparsers.argparse.ArgumentParser(
            formatter_class=argparse.RawDescriptionHelpFormatter,
            description="Generates vocabulary")

    parser.add_argument(
        '--train_file', type=argparse.FileType('r'), default=sys.stdin,
        metavar='PATH',
        help="Input file (default: standard input).")

    parser.add_argument(
        '--vocab_file', type=argparse.FileType('w'), default=sys.stdout,
        metavar='PATH',
        help="Output file (default: standard output)")

    return parser

def get_vocab(train_file, vocab_file):

    c = Counter()

    for line in train_file:
        for word in line.strip('\r\n ').split(' '):
            if word:
                c[word] += 1

    for key,f in sorted(c.items(), key=lambda x: x[1], reverse=True):
        vocab_file.write(key+" "+ str(f) + "\n")

if __name__ == "__main__":

    # python 2/3 compatibility
    if sys.version_info < (3, 0):
        sys.stderr = codecs.getwriter('UTF-8')(sys.stderr)
        sys.stdout = codecs.getwriter('UTF-8')(sys.stdout)
        sys.stdin = codecs.getreader('UTF-8')(sys.stdin)
    else:
        sys.stderr = codecs.getwriter('UTF-8')(sys.stderr.buffer)
        sys.stdout = codecs.getwriter('UTF-8')(sys.stdout.buffer)
        sys.stdin = codecs.getreader('UTF-8')(sys.stdin.buffer)

    parser = create_parser()
    args = parser.parse_args()

    if args.train_file.name != '<stdin>':
        args.train_file = codecs.open(args.train_file.name, encoding='utf-8')
    if args.vocab_file.name != '<stdout>':
        args.vocab_file = codecs.open(args.vocab_file.name, 'w', encoding='utf-8')

    get_vocab(args.train_file, args.vocab_file)