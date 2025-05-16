import time

from ._interfaces import IPluginConfig, IPluginRuntime, IPluginControl
from ._plugin_metadata_property_entity import MetadataPropertyEntity

from ..channel import DataChannel
from ..message import Message


class PluginBase(IPluginConfig, IPluginRuntime, IPluginControl):
    __channels: [str, DataChannel] = {}
    __properties: [str, MetadataPropertyEntity] = {}

    def __init__(self):
        self.__channels = {}
        self.__properties = {}

    def add_property(self, property_name, property_type, default_value=None, select_values=None):
        self.__properties[property_name] = MetadataPropertyEntity(
            property_name,
            property_type,
            default_value,
            select_values
        )

    def del_property(self, property_name):
        del (self.__properties[property_name])

    def get_property(self, property_name):
        return self.__properties[property_name]

    def get_properties(self):
        return self.__properties

    def get_property_value(self, property_name) -> any:
        return self.__properties[property_name].value

    def set_property_value(self, property_name: str, value: any):
        self.__properties[property_name].value = value

    def get_config(self):
        pass

    def set_config(self):
        pass

    def set_channel(self, channel_name, channel):
        if channel_name in self.__channels:
            raise KeyError(f'Channel {channel_name} already exists')
        self.__channels[channel_name] = channel

    def get_channel(self, channel_name):
        if channel_name not in self.__channels:
            raise KeyError(f'Channel {channel_name} not exists')
        return self.__channels[channel_name]

    def remove_channel(self, channel_name):
        if channel_name not in self.__channels:
            raise KeyError(f'Channel {channel_name} not exists')
        del (self.__channels[channel_name])

    def send_data(self, channel_name, data: any):
        msg = Message(data, time.time())
        channel = self.get_channel(channel_name)
        channel.enqueue(msg)

    def get_data(self, channel_name) -> Message:
        channel = self.get_channel(channel_name)
        msg = channel.dequeue()
        return msg

    def run(self): ...

    def stop(self): ...

    def pause(self): ...

    def resume(self): ...

    def notify(self, data): ...

    def pre_install(self, data): ...

    def post_install(self, data): ...

    def pre_uninstall(self, data): ...

    def post_uninstall(self, data): ...
