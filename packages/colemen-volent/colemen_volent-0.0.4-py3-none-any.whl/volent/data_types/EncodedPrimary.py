# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-import

from dataclasses import dataclass
from typing import Iterable
import colemen_utils as c
import volent.settings as _settings
import volent.settings.types as _t
from volent.exceptions import ValidationError
from volent.data_types.TypeBase import TypeBase as _type_base

@dataclass
class EncodedPrimary(_type_base):




    def __init__(self,data_length:int=None) -> None:
        super().__init__(data_length)
        self.min_data_length = 0
        self.max_data_length = 65535
        self.sql_type_name = "BIGINT"
        self.python_data_type = (int,str)
        self.open_api_data_type = "string"

        self._validate_data_length(data_length)


    def serialized_value(self,value):
        if isinstance(value,(str)):
            return value
        return c.string.string_encode_int(value)

    def deserialized_value(self,value):
        if isinstance(value,(int)):
            # return value
            raise ValidationError(f"Failed to decode the id {value}")
        
        val = c.string.string_decode_int(value)
        if isinstance(val,(int)):
            return val
        raise ValidationError(f"Failed to decode the id {value}")


    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} : {self.data_length}>"