# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-import

from dataclasses import dataclass
from typing import Iterable
import colemen_utils as c
import volent.settings as _settings
import volent.settings.types as _t
from volent.data_types.TypeBase import TypeBase as _type_base
from volent.exceptions import ValidationError


@dataclass
class BigInt(_type_base):




    def __init__(self,data_length:int=None) -> None:
        super().__init__(data_length)
        self.min_data_length = 0
        self.max_data_length = 65535
        self.sql_type_name = "BIGINT"
        self.python_data_type = (int)
        self.open_api_data_type = "integer"

        self._validate_data_length(data_length)


    def serializer(self,value,field_name:str=None):
        # print(f"field_name:{field_name}")
        if isinstance(value,(str)):
            return self.deserialized_value(value,field_name)
        if isinstance(value,int):
            return self.serialized_value(value,field_name)

    def serialized_value(self,value,field_name:str=None):
        if isinstance(value,(int)):
            return value

        if value is None:
            return value

        if isinstance(value,(str)):
            if c.valid.numeric_only(value):
                value = int(value)
        if isinstance(value,(float)):
            value = int(value)

        if isinstance(value,(int)) is False:
            raise ValidationError(f"Failed to serialize {value} to integer.",field_name)

        return value

    def deserialized_value(self,value,field_name:str=None):
        if isinstance(value,(int)):
            return value
        if value is None:
            return value
        if isinstance(value,(str)):
            if c.valid.numeric_only(value):
                try:
                    return int(value)
                except ValueError as e:
                    raise ValidationError(f"Invalid value provided: {value}.",field_name)
        if isinstance(value,(int)) is False:
            raise ValidationError(f"Failed to deserialize {value} to integer.",field_name)



    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} : {self.data_length}>"