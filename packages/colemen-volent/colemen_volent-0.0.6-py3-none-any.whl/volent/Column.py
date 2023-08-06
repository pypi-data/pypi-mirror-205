# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-import


from dataclasses import dataclass
from typing import Iterable

import colemen_utils as _c

import volent.settings.types as _t
import volent.settings as _settings
from volent.mixins import MySQLGeneratorMixin
from volent.UniqueConstraint import UniqueConstraint as _uniqueConstraint
from volent.FullTextIndex import FullTextIndex as _fullTextIndex

@dataclass
class Column(MySQLGeneratorMixin):
    model:_t.model_type = None

    name:str = None
    data_type:_t.type_base_type = None
    default = _settings.types.no_default
    on_update = _t.undefined
    '''The value to set this column to when an update is performed'''
    on_insert = _t.undefined
    '''The value to set this column to when an insertion is performed'''
    nullable:bool = None
    comment:str = None
    is_foreign_key:bool = None
    is_primary:bool = None
    auto_increment = None
    _unique:bool = None
    _fulltext:bool = None
    is_private:bool = None
    dump_only:bool = None

    # relationship:Iterable[_t.relationship_type] = None
    # _column_value = "__NO_VALUE__"
    _column_value = _t.undefined

    def __init__(
        self,
        data_type:str,
        name:str=None,
        nullable:bool=False,
        comment:str=None,
        is_foreign_key:bool=False,
        is_primary:bool=False,
        auto_increment:bool=False,
        unique:bool=False,
        fulltext:bool=False,
        default=_settings.types.no_default,
        dump_only=False,
        on_update=_t.undefined,
        on_insert=_t.undefined,
        ):
        '''
            Create a column instance.

            ----------

            Arguments
            -------------------------
            `data_type` {str,data_type}
                The data_type that this column uses.
            [`name`=None] {str}
                The name of this column, if not provided, the variable name will be used from its declaration in the model

            [`nullable`=False] {bool}
                If True, the column will allow "NULL" values

            [`comment`=None] {str}
                The comment to add to the column in the database.

            [`is_foreign_key`=False] {bool}
                If True, this column should have an associated Relationship

            [`is_primary`=False] {bool}
                If True, this column will be treated as the primary index of the table.
                There can only be one of these.

            [`auto_increment`=False] {bool}
                if True, the column will be auto_incremented in the database.
                There can only be one of these

            [`unique`=False] {bool}
                If True, a unique constraint will be added to this column.

            [`fulltext`=False] {bool}
                If True, a fulltext index will be added to this column.

            [`default`=noDefault] {any}
                The default value to assign to this column if a value is not provided.

            [`dump_only`=False] {bool}
                If True, this column cannot be updated after insertion

            [`on_update`=undefined] {any}
                This value will be automatically set any time this column's row is updated.

            [`on_insert`=undefined] {any}
                This value will be automatically set when the column is inserted


            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 04-28-2023 10:12:26
            `memberOf`: Column
            `version`: 1.0
            `method_name`: column
            * @xxx [04-28-2023 10:19:39]: documentation for column
        '''

        self.name = name
        self.data_type = data_type
        self.default = default
        self.on_update = on_update
        self.on_insert = on_insert
        self._unique = unique
        self._fulltext = fulltext
        self.nullable = nullable

        self.comment = comment
        self.is_foreign_key = is_foreign_key
        self.is_primary = is_primary
        self.auto_increment = auto_increment
        self.dump_only = dump_only
        self._column_value = _t.undefined

    @property
    def summary(self):
        '''
            Get this Column's summary

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 04-18-2023 08:26:42
            `@memberOf`: Column
            `@property`: summary
        '''
        value = {
            "name":self.name,
            "data_type":self.data_type.summary,
            "default":self.default,
            "unique":self.unique,
            "fulltext":self.fulltext,
            "nullable":self.nullable,
            "comment":self.comment,
            "is_foreign_key":self.is_foreign_key,
            "is_primary":self.is_primary,
            "auto_increment":self.auto_increment,
            "dump_only":self.dump_only,
            "on_update":self.on_update,
            "on_insert":self.on_insert,
        }
        if self.default == _t.no_default:
            value['default'] = "no default"
        if self.on_update == _t.undefined:
            value['on_update'] = "no_on_update"
        if self.on_insert == _t.undefined:
            value['on_insert'] = "no_on_insert"
        return value

    def __call__(self, *args, **kwds):
        return self._column_value


    @property
    def dot_path(self):
        '''
            Get this Column's dot_path

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 04-14-2023 07:22:26
            `@memberOf`: Column
            `@property`: dot_path
        '''
        value = self.name
        if self.model is not None:
            value = f"{self.model.name}.{self.name}"
        return value


    @property
    def value(self):
        '''
            Get this Column's value

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 04-11-2023 14:49:51
            `@memberOf`: Column
            `@property`: value
        '''
        value = self._column_value
        if value == _t.undefined:
            if self.default != _t.no_default:
                value = self.default
                self._column_value = value
        return value

    @value.setter
    def value(self,value):
        '''
            Set the Column's value property

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 04-11-2023 14:54:15
            `@memberOf`: Column
            `@property`: value
        '''
        if value != self._column_value:
            self.model._saved = False
        self._column_value = value

    @property
    def serialized_value(self):
        '''
            Get this Column's serialized_value

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 03-27-2023 11:05:37
            `@memberOf`: Column
            `@property`: serialized_value
        '''
        value = self.value
        if hasattr(self.data_type,"__serialize"):
            return self.data_type.__serialize(value)
        return value

    @property
    def deserialized_value(self):
        '''
            Get this Column's deserialized_value

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 03-27-2023 11:05:37
            `@memberOf`: Column
            `@property`: serialized_value
        '''
        value = self.value
        if hasattr(self.data_type,"serializer"):
            return self.data_type.serializer(value,self.name)
        if hasattr(self.data_type,"__deserialize"):
            return self.data_type.__deserialize(value)
        if hasattr(self.data_type,"deserialized_value"):
            return self.data_type.deserialized_value(value)
        return value

    @property
    def unique(self):
        '''
            Get this Column's unique value.
            
            This will also create a unique constraint instance

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 04-28-2023 10:23:37
            `@memberOf`: Column
            `@property`: unique
        '''
        value = self._unique
        if value is True:
            # name = f"UQ_{_c.rand.rand()}"
            name = f"UQ_{self.model.name}_{self.name}"
            # if self.model.get_unique_constraint(name) is not None:
            #     return value
            comment = f"Ensure the {self.name} is unique."
            u = _uniqueConstraint(self,name,comment)
            # self.model.__setattr__(name,u)
            setattr(self.model,name,u)
        return value

    @property
    def fulltext(self):
        '''
            Get this Column's fulltext value

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 04-28-2023 10:23:37
            `@memberOf`: Column
            `@property`: unique
        '''
        value = self._unique
        if value is True:
            name = f"FT_{self.model.name}_{self.name}"
            u = _fullTextIndex(self,name)
            setattr(self.model,name,u)
        return value

    def __repr__(self):
        return f"<{self.__class__.__name__} : {self.name} {self.data_type.python_data_type} {self.value}>"
