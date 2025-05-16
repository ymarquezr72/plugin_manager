import importlib
import subprocess
import sys

from pathlib import Path
from domain.exceptions import InvalidPluginStructureError, DependencyInstallationError


def validate_extracted_plugin(plugin_dir: str) -> Path:
    plugin_dir = Path(plugin_dir)
    if not (plugin_dir / "__init__.py").exists():
        raise InvalidPluginStructureError("Módulo principal no encontrado")
    return plugin_dir


def load_plugin_module(plugin_dir: Path):
    sys.path.insert(0, str(plugin_dir.parent))
    try:
        module = importlib.import_module(plugin_dir.name)
    except ImportError as e:
        raise InvalidPluginStructureError(f"Error cargando módulo: {str(e)}") from e
    finally:
        sys.path.pop(0)
    return module


def get_plugin_info(module) -> dict[str, any]:
    if not hasattr(module, 'get_info'):
        raise InvalidPluginStructureError("Función get_info() no encontrada")
    info = module.get_info()
    if not isinstance(info, dict):
        raise InvalidPluginStructureError("get_info() debe retornar un diccionario")
    return info


def validate_entry_points(module, plugin_info: dict) -> dict[str, str]:
    entry_points = plugin_info.get('entry_points', {})
    required = {'config_class', 'runtime_class', 'control_class'}
    if not required.issubset(entry_points.keys()):
        raise InvalidPluginStructureError("Entry points requeridos faltantes")

    validated = {}
    for ep_name, ep_data in entry_points.items():
        cls = ep_data.get('class')
        if not cls or not hasattr(module, cls.__name__):
            raise InvalidPluginStructureError(f"Clase {ep_name} inválida")
        validated[ep_name] = f"{module.__name__}.{cls.__name__}"
    return validated


def install_dependencies(plugin_dir: Path) -> None:
    req_file = plugin_dir / "requirements.txt"
    if req_file.exists():
        try:
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "-r", str(req_file)],
                check=True,
                capture_output=True
            )
        except subprocess.CalledProcessError as e:
            raise DependencyInstallationError(e.stderr.decode()) from e
