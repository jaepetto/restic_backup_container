import logging
import os.path
import subprocess
import sys
from typing import List

from decouple import config

logger = logging.getLogger(__name__)

DATA_PATH = config("DATA_PATH", default="/data")
AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID", default="")
AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY", default="")
RESTIC_REPOSITORY = config("RESTIC_REPOSITORY", default="")
RESTIC_PASSWORD = config("RESTIC_PASSWORD", default="")
RESTIC_ACTION = config("RESTIC_ACTION", default="")
IONICE_CLASS = config("IONICE_CLASS", default="2")
NICE_LEVEL = config("NICE_LEVEL", default="19")


def checkResticAvailability() -> None:
    """checks that restic is available at /usr/local/bin/restic"""
    logger.info("Checking restic availability at /usr/local/bin/restic")
    exists = os.path.isfile("/usr/local/bin/restic")
    if exists:
        logger.info("restic is available")
    else:
        logger.error("restic is not available")
        raise FileNotFoundError("restic is not available")


def checkDataPath() -> None:
    """Checks that the data path is available and readable"""
    exists = os.path.isdir(DATA_PATH)
    if exists:
        logger.info(f"Data path {DATA_PATH} is available")
    else:
        logger.error(f"Data path {DATA_PATH} is not available")
        raise FileNotFoundError(f"Data path {DATA_PATH} is not available")


def checkS3Credentials() -> None:
    logger.info("Checking S3 credentials")
    if AWS_ACCESS_KEY_ID == "":
        logger.error("AWS_ACCESS_KEY_ID is not set")
        raise ValueError("AWS_ACCESS_KEY_ID is not set")
    else:
        logger.info(
            "AWS_ACCESS_KEY_ID: {AWS_ACCESS_KEY_ID}".format(
                AWS_ACCESS_KEY_ID=AWS_ACCESS_KEY_ID
            )
        )

    if AWS_SECRET_ACCESS_KEY == "":
        logger.error("AWS_SECRET_ACCESS_KEY is not set")
        raise ValueError("AWS_SECRET_ACCESS_KEY is not set")
    else:
        logger.info(
            "AWS_SECRET_ACCESS_KEY: {AWS_SECRET_ACCESS_KEY}".format(
                AWS_SECRET_ACCESS_KEY="*" * len(AWS_SECRET_ACCESS_KEY)
            )
        )

    if RESTIC_REPOSITORY == "":
        logger.error("RESTIC_REPOSITORY is not set")
        raise ValueError("RESTIC_REPOSITORY is not set")
    else:
        logger.info(
            "RESTIC_REPOSITORY: {RESTIC_REPOSITORY}".format(
                RESTIC_REPOSITORY=RESTIC_REPOSITORY
            )
        )


def checkResticPassword() -> None:
    logger.info("Checking RESTIC_PASSWORD")
    if RESTIC_PASSWORD == "":
        logger.error("RESTIC_PASSWORD is not set")
        raise ValueError("RESTIC_PASSWORD is not set")
    else:
        logger.info(
            "RESTIC_PASSWORD: {RESTIC_PASSWORD}".format(
                RESTIC_PASSWORD="*" * len(RESTIC_PASSWORD)
            )
        )


def checkResticAction() -> None:
    logger.info(
        "Checking RESTIC_ACTION: {RESTIC_ACTION}".format(RESTIC_ACTION=RESTIC_ACTION)
    )
    possible_actions = [
        "backup",
        "restore",
        "check",
        "forget",
        "prune",
        "ls",
        "unlock",
        "version",
        "init",
        "help",
    ]
    if RESTIC_ACTION in possible_actions:
        logger.info("RESTIC_ACTION is valid")
    else:
        logger.error("RESTIC_ACTION is not valid")
        raise ValueError("RESTIC_ACTION is not valid")


def runHelp() -> None:
    logger.info("Running help")
    runRestic(["--help"])


def runInit() -> None:
    logger.info("Running init")
    runRestic(["init"])


def runBackup() -> None:
    logger.info("Running backup")
    runRestic(["backup", "--exclude", "**/.Trash**", "--exclude", "**/.snapshot/**", "-vv", DATA_PATH])


def runCheck() -> None:
    logger.info("Running check")
    runRestic(["check", "--read-data"])


def runList() -> None:
    logger.info("Running list")
    runRestic(["snapshots"])


def runForget() -> None:
    logger.info("Running forget")
    runRestic(
        [
            "forget",
            "--keep-daily",
            "7",
            "--keep-weekly",
            "5",
            "--keep-monthly",
            "12",
            "--keep-yearly",
            "75",
        ]
    )


def runPrune() -> None:
    logger.info("Running prune")
    runRestic(["prune"], with_host=False)


def runRestic(args: List[str], with_host: bool = True) -> None:
    logger.info("Running restic")
    baseArgs = ["ionice", "-c{}".format(IONICE_CLASS), "nice", "-n{}".format(NICE_LEVEL), "/usr/local/bin/restic"]
    if with_host:
        baseArgs += ["--host", "docker"]

    # completed_process = subprocess.run(baseArgs + args, capture_output=True, text=True)
    all_args = baseArgs + args
    logger.debug("Running restic with args: {all_args}".format(all_args=all_args))
    completed_process = subprocess.run(all_args)
    if completed_process.returncode == 0:
        logger.info("Restic completed successfully")
        logger.info(completed_process.stdout)
    else:
        logger.error("Restic failed")
        logger.error(completed_process.stderr)
        raise RuntimeError("Restic failed")


def main() -> None:
    checkResticAvailability()
    checkDataPath()
    checkS3Credentials()
    checkResticPassword()
    checkResticAction()

    if RESTIC_ACTION == "help":
        runHelp()
    elif RESTIC_ACTION == "init":
        runInit()
    elif RESTIC_ACTION == "backup":
        runBackup()
    elif RESTIC_ACTION == "check":
        runCheck()
    elif RESTIC_ACTION == "ls":
        runList()
    elif RESTIC_ACTION == "forget":
        runForget()
    elif RESTIC_ACTION == "prune":
        runPrune()
    else:
        raise NotImplementedError(
            "RESTIC_ACTION {RESTIC_ACTION} not implemented".format(
                RESTIC_ACTION=RESTIC_ACTION
            )
        )


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        stream=sys.stdout,
    )
    main()
