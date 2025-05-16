import unittest

from domain.interfaces import IPluginLogger
from infrastructure.logger import ConsoleLogger


class TestPLoggerConsole(unittest.TestCase):
    def setUp(self):
        self.logger: IPluginLogger = ConsoleLogger("console_logger")

    def test_logger_console(self):
        self.logger.info("Console Info")
        self.logger.error("Console Error")
        self.logger.warning("Console Warning")
        self.logger.debug('Console Debug')
        self.logger.critical('Console Critical')
