import os
import tempfile
import unittest
from pathlib import Path

from domain.exceptions import PluginExtractionError
from domain.helpers import extract_plugin


class TestPluginManifest(unittest.TestCase):

    def setUp(self):
        self.source_dir: Path = Path("C:\\Users\\usuario\\Projects\\plugins_arch\\plugins_manager_core\\tests"
                                     "\\tar_files")

    def test_extract_file(self):
        file_to_extract: Path = self.source_dir / "test_plugin_1.0.0.tar.gz"
        with tempfile.TemporaryDirectory() as tmp_dir:
            extract_plugin(str(file_to_extract), tmp_dir)
            file_check = Path(tmp_dir) / "__init__.py"
            self.assertEqual(file_check.is_file(), True)

        file_to_extract: Path = self.source_dir / "test_plugin_ws_1.0.0.tar.gz"
        with tempfile.TemporaryDirectory() as tmp_dir:
            extract_plugin(str(file_to_extract), tmp_dir)
            file_check = Path(tmp_dir) / "__init__.py"
            self.assertEqual(file_check.is_file(), True)

    def test_invalid_extract_file(self):
        file_to_extract: Path = self.source_dir / "test_plugin_bad_3.0.0.tar.gz"
        with self.assertRaises(PluginExtractionError):
            with tempfile.TemporaryDirectory() as tmp_dir:
                extract_plugin(str(file_to_extract), tmp_dir)

    def test_invalid_file_not_found(self):
        file_to_extract: Path = self.source_dir / "test_plugin_bad_4.0.0.tar.gz"
        with self.assertRaises(PluginExtractionError):
            with tempfile.TemporaryDirectory() as tmp_dir:
                extract_plugin(str(file_to_extract), tmp_dir)
