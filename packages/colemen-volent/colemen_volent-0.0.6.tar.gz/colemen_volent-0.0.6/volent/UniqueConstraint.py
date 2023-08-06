# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-import

from dataclasses import dataclass
from typing import Iterable, Union
import colemen_utils as c
import volent.settings as _settings
import volent.settings.types as _t
from volent.mixins.MySQLGeneratorMixin import MySQLGeneratorMixin

@dataclass
class UniqueConstraint(MySQLGeneratorMixin):
    main:_t._main_type = None
    # database:_t.database_type = None
    model:_t.model_type = None
    name:str = None
    comment:str = None
    columns:Iterable[_t.column_type] = None
    comment:str = None




    def __init__(
        self,
        columns:Iterable[_t.column_type],
        name:str=None,
        comment:str=None,
        ):
        '''
            Create a unique constraint instance.

            ----------

            Arguments
            -------------------------
            `Columns` {list,column}
                A column or list of columns to create a unique constraint on.

            `name` {str}
                The name of this unique constraint. This name must be unique through out the database.

            `comment` {str}
                The comment to add to the unique constraint in the database.


            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 04-28-2023 09:59:09
            `memberOf`: UniqueConstraint
            `version`: 1.0
            `method_name`: UniqueConstraint
            * @xxx [04-28-2023 10:01:29]: documentation for UniqueConstraint
        '''
        self.name = name
        self.comment = comment
        self.columns = c.arr.force_list(columns)



        # _parse_parent(self,parent)


    @property
    def summary(self):
        '''
            Get this UniqueConstraint's summary

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 03-23-2023 14:53:39
            `@memberOf`: UniqueConstraint
            `@property`: summary
        '''
        value = {
            "name":self.name,
            "comment":self.comment,
            "columns":[x.name for x in self.columns],
        }
        return value



    def __hash__(self):
        col_names = [x.name for x in self.columns]
        val = col_names.append(self.name)
        return hash(val)

    def __eq__(self,other):
        if isinstance(other,UniqueConstraint):
            return self.__hash__() == other.__hash__()
        return False

