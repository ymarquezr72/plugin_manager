import pandas as pd

from domain.base_plugin import PluginBase


class TestPluginModule(PluginBase):

    def __init__(self):
        super().__init__()
        self.add_property("csv_pathname", "string")
        self.add_property("csv_filename", "string")
        self.add_property("csv_separator", "string")
        self.add_property("csv_delimiter", "string")
        self.add_property("csv_header", "boolean")
        self.add_property("csv_double_quote", "boolean")

    def run(self):
        try:
            filename = f"{self.get_property_value('csv_pathname')}/{self.get_property_value('csv_filename')}"
            df = pd.read_csv(
                filename,
                sep=self.get_property_value('csv_separator'),
                doublequote=self.get_property_value('csv_double_quote'),
                header=0 if self.get_property_value('csv_header') else None
            )

            data = f"START-PROCESS"
            self.send_data("output_channel", data)

            for index, row in df.iterrows():
                data = {"description": row["description"], "sequence": row["sequence"]}
                self.send_data("output_channel", data)

            data = f"END-PROCESS"
            self.send_data("output_channel", data)
        except Exception as e:
            print(e)
