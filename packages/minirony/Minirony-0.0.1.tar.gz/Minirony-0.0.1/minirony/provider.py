from pyspark.sql.types import *
from minirony.manager import EnvironmentManager
import json

environment_manager = EnvironmentManager()


class DataTypeSparkProvider:
    def __init__(self):
        self.type_dict = {
            "string": StringType(),
            "date": DateType(),
            "timestamp": TimestampType(),
            "int": IntegerType(),
            "long": LongType(),
            "double": DoubleType(),
            "binary": BinaryType(),
            "short": ShortType(),
            "numeric": DoubleType(),
            "decimal": DoubleType(),
        }

    def get_data_type(self, type):
        return self.type_dict[type]


data_type_provider = DataTypeSparkProvider()


class SchemaProvider:
    def __init__(self) -> None:
        self.schema_env = environment_manager.get_schema()

    def get_partition_by(self):
        return environment_manager.get_partition_by()

    def get_date_partition_by(self):
        return environment_manager.get_date_partition_by()

    def get_entity(self):
        return environment_manager.get_entity()

    def get_schema(self):
        schema_dict = json.loads(self.schema_env)
        schema_fields = [
            StructField(name, dataType=data_type_provider.get_data_type(value))
            for name, value in schema_dict.items()
        ]
        return StructType(schema_fields)

    def get_window_id_key(self):
        return environment_manager.get_window_id_key()

    def get_equal_condition(self):
        return environment_manager.get_equal_condition()

    def drop_columns(self):
        return environment_manager.get_drop_columns().split(";")

    def transform_schema(self, schema):
        schema_fields = [
            StructField(name, dataType=data_type_provider.get_data_type(value))
            for name, value in schema.items()
        ]
        return StructType(schema_fields)
