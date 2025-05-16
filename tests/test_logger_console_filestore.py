import unittest
from pathlib import Path

from domain.interfaces import IPluginLogger
from infrastructure.logger import FileLogger, ConsoleFileLogger


class TestLoggerConsoleFilesystem(unittest.TestCase):

    def setUp(self):
        self.logger: IPluginLogger = ConsoleFileLogger(
            "filesystem_logger",
            Path("console_filesystem_registro_test.log"),

        )

    def test_logger_console_filesystem(self):
        self.logger.info("Console Filesystem Info")
        self.logger.error("Console Filesystem Error")
        self.logger.warning("Console Filesystem Warning")
        self.logger.debug('Console Filesystem Debug')
        self.logger.critical('Console Filesystem Critical')
