import logging
import subprocess

__all__ = ["Shell"]
logger = logging.getLogger("ennie.shell")


class Shell:
    def __init__(self, host, dryrun, debug):
        self.host = host
        self.dryrun = dryrun
        self.debug = debug

    def run(self, command):
        logger.debug("Host is %s,, Dryrun=%s Command is %s", self.host, self.dryrun, command)
        cmd = command

        if self.host:
            logger.debug("Run @%s", self.host)
            option = ''
            if self.debug == 0:
                option = '-v'

            cmd = "ssh -q %s " \
                  "-o StrictHostKeyChecking=no " \
                  "-o UserKnownHostsFile=/dev/null " \
                  "-o PasswordAuthentication=no " \
                  "%s %s" \
                  % (option, self.host, command)
        else:
            logger.debug("Run locally.")

        if self.dryrun:
            print("Command is:%s" % cmd)
            return

        (code, result) = self._run_cmd(cmd)

        logger.info("Result:%s,%s", code, result)

        return code, result

    @staticmethod
    def _run_cmd(command):
        logger.debug("Executing:%s", command)
        result = None
        code = 0
        try:
            result = subprocess.check_output(command, shell=True, universal_newlines=True)
            # , stderr=subprocess.DEVNULL)
        except subprocess.CalledProcessError as e:
            code = e.returncode

        return code, result


