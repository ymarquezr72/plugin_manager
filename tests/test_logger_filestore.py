import unittest
from pathlib import Path

from domain.interfaces import IPluginLogger
from infrastructure.logger import FileLogger


class TestLoggerFilesystem(unittest.TestCase):

    def setUp(self):
        self.logger: IPluginLogger = FileLogger(
            "filesystem_logger",
            Path("registro_test.log"),

        )

    def test_logger_filesystem(self):
        self.logger.info("Filesystem Info")
        self.logger.error("Filesystem Error")
        self.logger.warning("Filesystem Warning")
        self.logger.debug('Filesystem Debug')
        self.logger.critical('Filesystem Critical')
