from pathlib import Path

import logging

from .logger import LogHandler, LogSeverity


def initializeLogger(logLevel: int, logPath: Path) -> None:
    consoleFormatter = logging.Formatter(
        fmt = "{levelname}: {message}",
        style = "{",
    )
    consoleHandler = LogHandler.instance()
    consoleHandler.setLevel(LogSeverity(logLevel).stdSeverity)
    consoleHandler.setFormatter(consoleFormatter)

    fileFormatter = logging.Formatter(
        fmt = "%(asctime)s %(levelname)s: %(message)s",
        datefmt= "%Y-%m-%d %H:%M:%S",
        style = "%",
    )
    fileHandler = logging.FileHandler(logPath)
    fileHandler.setLevel(logging.DEBUG)
    fileHandler.setFormatter(fileFormatter)

    logging.basicConfig(
        level = logging.NOTSET,
        force = True,
        handlers = [
            consoleHandler,
            fileHandler
        ]
    )
