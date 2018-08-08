import sys
import os
import argparse

from .watcher import Watcher
from .cache import LRUCache


def start_watching(args):
    if not os.path.exists(args.path):
        sys.exit("{} doesn't exist".format(args.path))

    if not os.path.isdir(args.path):
        sys.exit("{} is not a directory".format(args.path))
        
    cache = LRUCache(args.path, args.size)
    w = Watcher(args.path, cache)
    w.run()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='File directory cache')
    parser.add_argument(
        '--policy', dest='policy', action='store',
        help='Eviction policy', default="lru", choices=["lru"])

    parser.add_argument(
        '--size', type=int, dest='size',
        required=True, action='store', help='Max size for the folder')

    parser.add_argument('path', metavar='path', help='Path to use as cache')
    parser.set_defaults(func=start_watching)

    args = parser.parse_args()
    if len(vars(args)):
        args.func(args)
    else:
        parser.print_help()
