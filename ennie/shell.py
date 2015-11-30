import logging
import subprocess

__all__ = ["shell"]


logger = logging.getLogger("ennie.shell")

def shell(host, command, dryrun):
    logger.debug("Host is %s, Command is %s, Dryrun=%s",host, command, dryrun)
    cmd = command

    if host :
        logger.debug("Run @%s", host)
        cmd = "ssh -v %s %s" % (host, command)
    else:
        logger.debug("Run locally.")

    if dryrun:
        print("Command is:%s" % cmd)
        return

    (result, err) = runCmd(cmd)

    if err:
        logger.info(err)
    else:
        logger.info("Result:%s", result)


def runCmd(command):
    logger.debug("Executing:%s", command)
    result = None
    err = None
    try:
        result = subprocess.check_output(command, shell=True, universal_newlines=True)#, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        #logger.exception(e)
        err = e

    return result, err


