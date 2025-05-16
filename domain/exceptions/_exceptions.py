class PluginError(Exception):
    """Base exception for plugin related errors"""


class PluginVersionError(PluginError):
    """Validation error for version plugin"""


class PluginValidationError(PluginError):
    """Validation error for plugin data"""


class PluginEntrypointError(PluginError):
    """Validation error for plugin data"""


class PluginAlreadyRegisteredError(PluginError):
    """Plugin is already registered"""

    def __init__(self, plugin_id):
        super().__init__(f"Plugin {plugin_id.name}@{plugin_id.version} ya registrado")


class PluginStorageRegisterError(PluginError):
    """Plugin not registered"""

    def __init__(self, plugin_id):
        super().__init__(f"Existe un problema al registrar el plugin {plugin_id.name}@{plugin_id.version}")


class PluginRegistrationError(PluginError):
    """Plugin registration"""


class PluginUnregistrationError(PluginError):
    """Plugin registration"""


class PluginUpdateError(PluginError):
    """Plugin registration"""


class PluginExtractionError(PluginError):
    """Plugin registration"""


class PluginStorageUnregisterError(PluginError):
    """Plugin not registered"""

    def __init__(self, plugin_id):
        super().__init__(f"Existe un problema al eliminat el registro del plugin {plugin_id.name}@{plugin_id.version}")


class PluginNotFoundError(PluginError):
    """Plugin not found"""

    def __init__(self, plugin_id):
        super().__init__(f"Plugin {plugin_id.name}@{plugin_id.version} no encontrado")


class InvalidPluginStructureError(PluginError):
    """Invalid plugin structure"""


class InterfaceImplementationError(PluginError):
    """Interface not properly implemented"""


class DependencyInstallationError(PluginError):
    """Error installing dependencies"""


class PluginIntegrityError(PluginError):
    """Error of plugin integrity"""
