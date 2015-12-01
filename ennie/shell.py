import logging
import subprocess

__all__ = ["shell"]
logger = logging.getLogger("ennie.shell")


def shell(host, command, dryrun, debug):
    logger.debug("Host is %s, Command is %s, Dryrun=%s", host, command, dryrun)
    cmd = command

    if host:
        logger.debug("Run @%s", host)
        option = ''
        if debug:
            option = '-v'

        cmd = "ssh -q %s " \
              "-o StrictHostKeyChecking=no " \
              "-o UserKnownHostsFile=/dev/null " \
              "-o PasswordAuthentication=no " \
              "%s %s" \
              % (option, host, command)
    else:
        logger.debug("Run locally.")

    if dryrun:
        print("Command is:%s" % cmd)
        return

    (code, result) = run_cmd(cmd)

    logger.info("Result:%s,%s", code, result)

    return code, result


def run_cmd(command):
    logger.debug("Executing:%s", command)
    result = None
    code = 0
    try:
        result = subprocess.check_output(command, shell=True, universal_newlines=True)  # , stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        code = e.returncode

    return code, result


