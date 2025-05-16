from dataclasses import dataclass


@dataclass
class MetadataPropertyEntity:
    property_name: str = ""
    property_type: str = ""
    default_value: any = None
    select_values: list = None
    value = None

    def __init__(self, name, ptype, default_value=None, select_values=None):
        self.property_name = name
        self.property_type = ptype
        self.default_value = default_value
        self.select_values = select_values
        self.value = None
