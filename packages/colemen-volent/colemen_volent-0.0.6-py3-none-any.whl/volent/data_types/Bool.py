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
class Bool(_type_base):


    def __init__(self) -> None:
        super().__init__()
        self.sql_type_name = "BOOLEAN"
        self.python_data_type = (bool)
        self.open_api_data_type = "boolean"


    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} >"


    def serializer(self,value,field_name:str=None):

        if isinstance(value,(bool)) is False:
            return self.deserialized_value(value,field_name)

        else:
            return self.serialized_value(value,field_name)



    def serialized_value(self,value,field_name:str=None):

        if isinstance(value,(bool)):
            return value

        value = c.types.bool_to_int(value)

        if isinstance(value,(int)) is False:
            raise ValidationError(f"Failed to serialize {value} to an integer.",field_name)

        return value

    def deserialized_value(self,value,field_name:str=None):

        if isinstance(value,(bool)):
            return value
        if value == _t.undefined or value == _t.no_default:
            return value
        if value is None:
            return value

        value = c.types.to_bool(value)

        if isinstance(value,(bool)) is False:
            raise ValidationError(f"Failed to serialize {value} to a boolean.",field_name)

        return value

    