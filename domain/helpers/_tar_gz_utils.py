import tarfile
from pathlib import Path

from domain.exceptions import PluginExtractionError


def extract_plugin(tar_gz_path: str, dest_dir: str) -> Path:
    try:
        with tarfile.open(tar_gz_path, "r:gz") as tar:
            members = tar.getmembers()
            root_dirs = {m.name.split("/")[0] for m in members if m.isdir()}
            if len(root_dirs) == 1:
                root_dir = root_dirs.pop()
                new_members = []
                for member in members:
                    if member.path.startswith(root_dir + "/"):
                        member.name = member.name[len(root_dir + "/"):]
                        new_members.append(member)
            else:
                new_members = members
            tar.extractall(path=dest_dir, members=new_members)
    except (tarfile.TarError, IOError) as e:
        raise PluginExtractionError(f"Error extrayendo plugin: {str(e)}") from e

    return Path(dest_dir)
