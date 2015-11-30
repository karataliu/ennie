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

    (result, err) = run_cmd(cmd)

    if err:
        logger.info(err)
    else:
        logger.info("Result:%s", result)

    return result, err


def run_cmd(command):
    logger.debug("Executing:%s", command)
    result = None
    err = None
    try:
        result = subprocess.check_output(command, shell=True, universal_newlines=True)  # , stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        err = e

    return result, err


