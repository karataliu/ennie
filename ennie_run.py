#!/usr/bin/env python
# This is to help run package management on multiple platforms

import argparse
import logging
import ennie

logger = logging.getLogger('ennie')

def initLogger():
    #formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s - %(message)s', '%Y-%m-%d %H:%M:%S', '%')
    formatter = logging.Formatter('[%(name)s,%(levelname)s] %(message)s', '%H:%M:%S')
    con = logging.StreamHandler()
    con.setFormatter(formatter)
    logging.getLogger('ennie').addHandler(con)


def getParser():
    parser = argparse.ArgumentParser(description='Helper on multiple platforms')
    parser.add_argument('--host','-t', help="specify the host to run on, will target localhost if not specified.")
    parser.add_argument('--verbose', '-v', action='store_true', help="Show debug information.")
    parser.add_argument('--dry-run', '-n', action='store_true', help="Show command only.")

    moduleParsers = parser.add_subparsers(metavar='MODULE', dest="module")
    moduleDetection = moduleParsers.add_parser('detection', help='do detection') #, aliases=['de']
    moduleDetection.add_argument('action', choices=['list', 'clear'])

    #sp = moduleParsers.add_parser('package', help='do packing')

    moduleShell = moduleParsers.add_parser('shell', help='execute command.')
    moduleShell.add_argument('command')

    return parser

def dispatch(args):
    moudle = None
    try:
        module = args.module
    except AttributeError:
        print("Must provide a module name.")
        exit(1)
    logger.debug("Dispatching module:%s", module)
    if module == 'shell':
        ennie.shell(args.host, args.command, args.dry_run)


def main():
    parser = getParser()
    args = parser.parse_args()
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    logger.debug("args: %s", args)
    dispatch(args)


if __name__ == '__main__':
    initLogger()
    main()
