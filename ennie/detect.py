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
    def __init__(self, host, dryrun, verbose):
        self.host = host
        self.dhost = self.host
        if not self.dhost:
            self.dhost = "localhost"
        self.dryrun = dryrun
        self.verbose = verbose

        self.data = self.load_data()

    def detect(self, action):
        logger.debug("Module: detection, Host:%s, Action:%s", self.host, action)

        if action == 'list':
            self.list_data()
        elif action == 'clear':
            self.clear_data()
        elif action == 'get':
            self.get_data()
        elif action == 'update':
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
        logger.debug("Begin detection")
        shell = ennie.Shell(self.host, self.dryrun, self.verbose)

        for cmd in package_detection:
            logger.debug("Testing:%s", cmd)
            (code, out) = shell.run(cmd)
            if code == 0:
                result["package.vendor"] = package_detection[cmd]
                break
        logger.debug("Detection result:%s", result)
        if not self.dryrun and result:
            self.data[self.dhost] = result
