#!/usr/bin/env python
# This is to help run package management on multiple platforms

import argparse
import logging
import ennie

logger = logging.getLogger('ennie')


def init_logger():
    # formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s - %(message)s', '%Y-%m-%d %H:%M:%S', '%')
    formatter = logging.Formatter('[%(name)s,%(levelname)s] %(message)s', '%H:%M:%S')
    con = logging.StreamHandler()
    con.setFormatter(formatter)
    logging.getLogger('ennie').addHandler(con)


def get_parser():
    parser = argparse.ArgumentParser(description='Helper on multiple platforms')
    parser.add_argument('--host', '-t', help="specify the host to run on, will target localhost if not specified.")
    parser.add_argument('--verbose', '-v', action='count', help="Show debug information.")
    # 0 for none, 1 for info, 2 for debug.
    parser.add_argument('--dry-run', '-n', action='store_true', help="Show command only.")

    module_parsers = parser.add_subparsers(metavar='MODULE', dest="module")
    module_detection = module_parsers.add_parser('detection', help='do detection')  # , aliases=['de']
    module_detection.add_argument('action', choices=['list', 'clear', 'get', 'update'])

    # sp = module_parsers.add_parser('package', help='do packing')

    module_shell = module_parsers.add_parser('shell', help='execute command.')
    module_shell.add_argument('command')

    return parser


def dispatch(args):
    module = args.module

    if not module:
        print("Must provide a module name.")
        exit(1)
    logger.debug("Dispatching module:%s", module)
    if module == 'shell':
        (err, result) = ennie.Shell(args.host, args.dry_run, args.verbose).run(args.command)
        if not err:
            print(result)
    elif module == 'detection':
        ennie.Detector(args.host, args.dry_run, args.verbose).detect(args.action)


def main():
    parser = get_parser()
    args = parser.parse_args()
    if not args.verbose:
        args.verbose = 0
    if args.verbose == 0:
        pass
    elif args.verbose == 1:
        logger.setLevel(logging.INFO)
    else:
        logger.setLevel(logging.DEBUG)
    logger.debug("args: %s", args)
    dispatch(args)


if __name__ == '__main__':
    init_logger()
    main()
