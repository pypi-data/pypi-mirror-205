# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-import


from dataclasses import dataclass
from typing import Iterable,OrderedDict


import colemen_utils as c


import volent.settings.types as _t
import volent.settings as _settings
from volent.Column import Column as _column
from volent.Relationship import Relationship as _relationship
from volent.UniqueConstraint import UniqueConstraint as _uniqueConstraint
from volent.mixins import MySQLGeneratorMixin
from collections import OrderedDict
from volent.exceptions import ValidationError


@dataclass
class Field:
    main = None
    # database:_t.database_type = None
    model:_t.model_type = None
    schema:_t.schema_type = None


    name:str = None

    # _fields:Iterable[_t.column_type] = None
    _description:str = None
    _example:str = None
    _ignore_null:bool = False
    column:_t.column_type = None


    required:bool = False
    nullable:bool = True
    default = None
    validators = None
    _data_type:_t.type_base_type = None
    _value = None
    '''The value associated to this field if there is no column'''
    _open_api_location:str = None


    def __init__(
        self,
        column:str=None,
        required:bool=False,
        nullable:bool=True,
        empty_string_is_null:bool=True,
        ignore_null:bool=False,
        default=_settings.types.no_default,
        validate=None,
        data_type:_t.type_base_type=None,
        description:str=None,
        example=None,
        open_api_location=None,
        ):
        '''
            Create a schema Field
            ----------

            Arguments
            -------------------------
            [`column`=None] {str}
                The name of the column that this field represents.
                The dot delimited path to the column

                If None, it will attempt to find a matching column in the model.

            [`required`=False] {bool}
                True if this field MUST have a value.
                
            [`nullable`=True] {bool}
                False if this field does not allow null values.

            [`empty_string_is_null`=True] {bool}
                Treat empty strings as None

            [`default`] {any}
                The default value to assign to this field

            [`validate`=None] {any}
                A list of validators to apply to this field

            [`ignore_null`=False] {bool}
                A list of validators to apply to this field

            [`description`=None] {any}
                A description of what this form stores.

            [`example`=None] {any}
                An example value of what this field stores.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 03-26-2023 09:34:14
            `memberOf`: Field
            `version`: 1.0
            `method_name`: Field
            * @xxx [04-14-2023 08:24:58]: documentation for Field
        '''
        self.column = column
        self.default = default
        self._description = description
        self._example = example
        self.required = required
        self.nullable = nullable
        self.empty_string_is_null = empty_string_is_null
        self._ignore_null = ignore_null
        self._data_type = data_type
        self._open_api_location = open_api_location

        self.validators = c.arr.force_list(validate,allow_nulls=False)


    @property
    def summary(self):
        '''
            Get this Model's summary

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 03-23-2023 14:39:08
            `@memberOf`: Model
            `@property`: summary
        '''
        value = {
            "name":self.name,
        }
        return value

    @property
    def dump_only(self):
        '''
            Get this Field's dump_only

            If True, this field can only be retrieved from the database and not inserted or updated.

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 04-18-2023 15:42:42
            `@memberOf`: Field
            `@property`: dump_only
        '''
        value = self.column.dump_only
        return value

    @property
    def value(self):
        '''
            Get this Field's value

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 03-25-2023 12:02:50
            `@memberOf`: Field
            `@property`: value
        '''
        value = None
        if self.column is not None:
            value = self.column.value
        else:
            value = self._value

        if isinstance(value,(str)):
            if len(value)==0 and self.empty_string_is_null:
                value = None
        return value

    @value.setter
    def value(self,value):
        '''
            Set the Field's value property

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 04-24-2023 08:52:25
            `@memberOf`: Field
            `@property`: value
        '''
        if self.column is not None:
            self.column.value = value
        else:
            self._value = value

    @property
    def data_type_instance(self):
        '''
            Get this Field's data_type_instance

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 04-25-2023 14:11:58
            `@memberOf`: Field
            `@property`: data_type_instance
        '''
        if self._data_type is not None:
            return self._data_type
        elif self.column is not None:
            return self.column.data_type

    @property
    def data_type(self):
        '''
            Get this Field's data_type

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 04-24-2023 08:42:36
            `@memberOf`: Field
            `@property`: data_type
        '''
        value = None
        if self._data_type is not None:
            if hasattr(self._data_type,"open_api_data_type"):
                value = self._data_type.open_api_data_type
        elif self.column is not None:
            value = self.column.deserialized_value()
        return value

    def validate_value(self,value):
        val = value
        if self._data_type is not None:
            if hasattr(self._data_type,"serializer"):
                val = self._data_type.serializer(val,self.name)
            if hasattr(self._data_type,"deserialized_value"):
                val = self._data_type.deserialized_value(val)


        if isinstance(val,self._data_type.python_data_type) is False:
            if self.nullable is True and val is None:
                pass
            else:
                raise ValidationError(f"{self.name} expects {self._data_type.python_data_type} types, {type(value)} provided.",self.name)

        # if self._less_than_data_len(val) is False:
        #     raise ValidationError(f"{self.name} is too long.",self.name)



        if self._is_null(val):
            raise ValidationError(f"{self.name} cannot be null.",self.name)


        for valid in self.validators:
            val = valid(val,self.name)

    def validate(self):
        '''
            Executes the validation methods on this field's value.

            if this field is not associated to a column, it will automatically use the validate_value method.
            This is important because columns require additional steps before they can be validated.


            ----------

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 04-24-2023 09:50:01
            `memberOf`: Field
            `version`: 1.0
            `method_name`: validate
            * @xxx [04-24-2023 09:54:22]: documentation for validate
        '''
        if self.value is None and self._ignore_null is True:
            return
        if self.column is None:
            return self.validate_value(self.value)
        # val = self.value
        val = self.column.deserialized_value
        # val = self.column.data_type.

        if isinstance(val,self.column.data_type.python_data_type) is False:
            if self.column.is_primary is True:
                pass
            elif self.column.nullable is True:
                pass
            else:
                raise ValidationError(f"{self.column.name} expects {self.column.data_type.python_data_type} types, {type(self.value)} provided.",self.name)

        if self._less_than_data_len(val) is False:
            raise ValidationError(f"{self.column.name} is too long.",self.name)

        if self._is_null(val):
            raise ValidationError(f"{self.name} cannot be null.",self.name)


        for valid in self.validators:
            val = valid(val,self.name)

    def _is_null(self,val):
        if isinstance(val,(str)):
            if len(val) == 0:
                val = None

        if self.nullable is False and self.value is None:
            return True
        return False

    def _less_than_data_len(self,val):
        if isinstance(self.column.data_type.data_length,(int)):
            val = str(val)
            length = len(val)
            if length > self.column.data_type.data_length:
                return False
        return True

        # "request_id":{
        #     "type":"string",
        #     "description":"The encoded request id",
        #     "example":encoded_id()
        # },

    def open_api_definition(self):
        if self.column is not None and self._description is None:
            self._description = self.column.comment
        data = {
            "type":self.data_type,
            "description":self._description,
            "example":self._example,
        }
        return data

    def open_api_data(self,loc:str="body")->dict:
        '''
            Generate a dictionary representation of this field that can be used with the open api library.

            ----------

            Arguments
            -------------------------
            [`loc`='body'] {str}
                Where the field's value can be found in a request ['body','path']

            Return {dict}
            ----------------------
            A dictionary of data about this field.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 04-24-2023 09:22:02
            `memberOf`: Field
            `version`: 1.0
            `method_name`: open_api_data.
            `throws`: ValueError - if the loc is not "body"/"path"
            * @xxx [04-24-2023 09:23:07]: documentation for open_api_data
        '''
        if self._open_api_location is not None:
            loc = self._open_api_location
        if loc not in _settings.control.open_api_param_locations:
            raise ValueError(f"{loc} is not a valid param location, expected: {','.join(_settings.control.open_api_param_locations)}")
        if self.column is not None and self._description is None:
            self._description = self.column.comment

        data = {
            "name": self.name,
            "description":self._description,
            "example":self._example,
            "in": loc,
            "type": self.data_type,
            "required": self.required,
        }
        if self.required is False:
            if self.default != _settings.types.no_default:
                data['default'] = self.default
            # else:
                # print(f"setting {self.name} required to True")
                # data['required'] = True

        return data


    @property
    def should_ignore(self):
        if self.value is None and self._ignore_null is True:
            return True
        return False

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} : {self.name}>"







