import os
import shutil


def plugin_copy_tree(from_path, to_path):
    os.makedirs(to_path, exist_ok=True)
    ignored_files = shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store", "~*")
    shutil.copytree(from_path, to_path, ignore=ignored_files, dirs_exist_ok=True)
