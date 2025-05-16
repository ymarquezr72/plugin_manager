import logging
from pathlib import Path

from domain.interfaces import IPluginLogger


class FileLogger(IPluginLogger):
    def __init__(self, name: str, filename: Path, level: int = logging.INFO):
        self.logger = logging.getLogger(name)
        handler = logging.FileHandler(filename)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(level)

    def log(self, level: int, message: object):
        self.logger.log(level=level, msg=message)

    def info(self, message: str, **kwargs) -> None:
        self.logger.info(message, **kwargs)

    def error(self, message: str, **kwargs) -> None:
        self.logger.error(message, **kwargs)

    def warning(self, message: str, **kwargs) -> None:
        self.logger.warning(message, **kwargs)

    def critical(self, message: str, **kwargs) -> None:
        self.logger.critical(message, **kwargs)

    def debug(self, message: str, **kwargs) -> None:
        self.logger.debug(message, **kwargs)
