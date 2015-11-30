import logging
import json
from os.path import expanduser,join

__all__ = ['detect']

logger = logging.getLogger("ennie.detect")
cache = join(expanduser("~"),'ennie.cache')
data = None


def detect(args):
    logger.debug("Module: detection, Action:%s", args.action)
    if args.action=='list':
        list()


def load():
    logger.debug("Loading from %s", cache)
    global data
    with open(cache) as f:
        data = json.load(f)


def save():
    with open(cache) as f:
        f.write(data)


def list():
    logger.debug("Run list:")
    print(data)


def clear1():
    pass


load()