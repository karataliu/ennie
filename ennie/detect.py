import logging
import json
from os.path import expanduser, join
import ennie

__all__ = ['Detector']

logger = logging.getLogger("ennie.detect")
dataFile = join(expanduser("~"), '.ennie.detect.cache')
package_detection = {
    'which pacman': 'pacman',
    'which apt-get': 'apt-get',
    'which yum': 'yum',
    'which zypper': 'zypper'
}


class Detector:
    def __init__(self, args):
        self.host = args.host
        self.dhost = self.host
        if not self.dhost:
            self.dhost = "localhost"
        self.action = args.action
        self.dry_run = args.dry_run
        self.debug = args.verbose

        self.data = self.load_data()

    def detect(self):
        logger.debug("Module: detection, Host:%s, Action:%s", self.host, self.action)

        if self.action == 'list':
            self.list_data()
        elif self.action == 'clear':
            self.clear_data()
        elif self.action == 'get':
            self.get_data()
        elif self.action == 'update':
            self.update_data()

    @staticmethod
    def load_data():
        logger.debug("Loading from %s", dataFile)
        det_data = {}
        try:
            with open(dataFile) as f:
                det_data = json.load(f)
        except FileNotFoundError:
            pass
        logger.debug("Loaded data: %s", det_data)

        return det_data

    def save_data(self):
        with open(dataFile, 'w') as f:
            json.dump(self.data, f)

    def list_data(self):
        logger.debug("Run list:")
        print(self.data)

    def clear_data(self):
        self.data = {}
        self.save_data()

    def get_data(self):
        logger.debug("Get data for %s", self.host)
        result = {}
        if self.dhost in self.data:
            result = self.data[self.dhost]

        logger.debug("Result is:%s", result)

        return result

    def update_data(self):
        self.do_detection()
        self.save_data()

    def do_detection(self):
        result = {}

        for cmd in package_detection:
            logger.debug("Testing:%s",cmd)
            (code, out) = ennie.shell(self.host, cmd, self.dry_run, self.debug)
            if code == 0:
                result["package.vendor"] = package_detection[cmd]
                break


        if not self.dry_run:
            self.data[self.dhost] = result
