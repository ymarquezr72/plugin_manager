from abc import abstractmethod, ABCMeta


class IPluginConfig(metaclass=ABCMeta):

    @abstractmethod
    def get_config(self): ...

    @abstractmethod
    def set_config(self): ...

    @abstractmethod
    def set_channel(self, channel_name, channel): ...

    @abstractmethod
    def get_channel(self, channel_name): ...

    @abstractmethod
    def remove_channel(self, channel_name): ...

    @abstractmethod
    def add_property(self, property_name, property_type, default_value=None, select_values=None): ...

    @abstractmethod
    def del_property(self, property_name): ...

    @abstractmethod
    def get_property(self, property_name): ...

    @abstractmethod
    def get_properties(self): ...

    @abstractmethod
    def get_property_value(self, property_name) -> any: ...

    @abstractmethod
    def set_property_value(self, property_name: str, value: any): ...


class IPluginRuntime(metaclass=ABCMeta):

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def pause(self):
        pass

    @abstractmethod
    def resume(self):
        pass


class IPluginControl(metaclass=ABCMeta):

    @abstractmethod
    def notify(self, data):
        pass

    @abstractmethod
    def pre_install(self, data):
        pass

    @abstractmethod
    def post_install(self, data):
        pass

    @abstractmethod
    def pre_uninstall(self, data):
        pass

    @abstractmethod
    def post_uninstall(self, data):
        pass

